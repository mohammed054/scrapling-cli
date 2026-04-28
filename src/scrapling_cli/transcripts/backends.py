from __future__ import annotations

import logging
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from threading import local
from typing import Protocol

from ..models import ContentItem, TranscriptOptions, TranscriptResult
from .cleaning import clean_plain_text, clean_subtitle_payload, merge_transcript_chunks

logger = logging.getLogger(__name__)

OPENAI_FILE_LIMIT_BYTES = 25 * 1024 * 1024
ASR_SEGMENT_SECONDS = 20 * 60
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


class TranscriptBackendError(RuntimeError):
    """Base transcript backend failure."""


class RetryableTranscriptError(TranscriptBackendError):
    """Failure that can be retried with backoff."""


class TranscriptBackend(Protocol):
    name: str

    def fingerprint(self, options: TranscriptOptions) -> str:
        ...

    def fetch(self, item: ContentItem, options: TranscriptOptions) -> TranscriptResult:
        ...


def _load_transcript_api_exceptions():
    try:
        from youtube_transcript_api import (
            CouldNotRetrieveTranscript,
            IpBlocked,
            PoTokenRequired,
            RequestBlocked,
        )
    except ImportError:  # pragma: no cover - exercised in runtime environments without deps
        return tuple()
    return CouldNotRetrieveTranscript, PoTokenRequired, IpBlocked, RequestBlocked


def _is_non_retryable_transcript_api_error(exc: Exception) -> bool:
    exception_types = _load_transcript_api_exceptions()
    return bool(exception_types) and isinstance(exc, exception_types)


def _language_matches(candidate: str, requested: str) -> bool:
    candidate_lower = candidate.lower()
    requested_lower = requested.lower()
    return candidate_lower == requested_lower or candidate_lower.startswith(f"{requested_lower}-")


def _select_track(track_map: dict, preferences: list[str]) -> tuple[str, dict] | None:
    if not track_map:
        return None
    for preference in preferences:
        for language, tracks in track_map.items():
            if _language_matches(language, preference):
                best = _select_best_track(tracks)
                if best:
                    return language, best
    for language in sorted(track_map):
        best = _select_best_track(track_map[language])
        if best:
            return language, best
    return None


def _select_best_track(tracks: list[dict]) -> dict | None:
    if not tracks:
        return None
    priority = {"vtt": 0, "srv3": 1, "srv2": 2, "srv1": 3, "json3": 4, "srt": 5, "ttml": 6}
    return sorted(tracks, key=lambda track: (priority.get(track.get("ext", ""), 99), track.get("url", "")))[0]


def _browser_headers(options: TranscriptOptions) -> dict[str, str]:
    language = (options.language or "en").strip() or "en"
    base_language = language.split("-", 1)[0]
    if language.lower().startswith("en"):
        accept_language = "en-US,en;q=0.9"
    else:
        accept_language = f"{language},{base_language};q=0.9,en;q=0.8"
    return {
        "User-Agent": BROWSER_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": accept_language,
        "Referer": "https://www.youtube.com/",
    }


def _yt_dlp_request_options(options: TranscriptOptions) -> dict:
    request_delay = max(0.0, options.request_delay_seconds)
    ydl_options = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "extractor_retries": max(1, options.retry_attempts),
        "http_headers": _browser_headers(options),
    }
    if request_delay > 0:
        ydl_options["sleep_interval_requests"] = request_delay
        ydl_options["sleep_interval_subtitles"] = request_delay
    return ydl_options


class YouTubeTranscriptApiBackend:
    name = "youtube_transcript_api"

    def __init__(self) -> None:
        self._thread_state = local()

    def _get_api(self, options: TranscriptOptions):
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError as exc:  # pragma: no cover - exercised in runtime environments without deps
            raise TranscriptBackendError("youtube-transcript-api not installed") from exc
        try:
            from requests import Session
        except ImportError:
            return YouTubeTranscriptApi()

        language = options.language or "en"
        cached_api = getattr(self._thread_state, "api", None)
        cached_language = getattr(self._thread_state, "language", None)
        if cached_api is not None and cached_language == language:
            return cached_api

        session = Session()
        session.headers.update(_browser_headers(options))
        session.headers.update({"Connection": "close"})
        api = YouTubeTranscriptApi(http_client=session)
        self._thread_state.api = api
        self._thread_state.language = language
        return api

    def fingerprint(self, options: TranscriptOptions) -> str:
        return f"{self.name}:{','.join(options.normalized_language_preferences())}"

    def fetch(self, item: ContentItem, options: TranscriptOptions) -> TranscriptResult:
        api = self._get_api(options)
        languages = options.normalized_language_preferences()
        try:
            transcript_list = api.list(item.id)
        except Exception as exc:  # noqa: BLE001
            if _is_non_retryable_transcript_api_error(exc):
                raise TranscriptBackendError(str(exc)) from exc
            raise RetryableTranscriptError(str(exc)) from exc

        transcript = None
        try:
            transcript = transcript_list.find_manually_created_transcript(languages)
        except Exception:  # noqa: BLE001
            transcript = None
        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(languages)
            except Exception:  # noqa: BLE001
                transcript = None
        if transcript is None:
            for available in transcript_list:
                try:
                    transcript = (
                        available.translate(options.language)
                        if getattr(available, "is_translatable", False) and options.language
                        else available
                    )
                except Exception:  # noqa: BLE001
                    transcript = available
                break

        if transcript is None:
            return TranscriptResult.unavailable(
                source=self.name,
                language=options.language,
                error="no transcript found",
                backend_fingerprint=self.fingerprint(options),
            )

        try:
            fetched = transcript.fetch()
        except Exception as exc:  # noqa: BLE001
            if _is_non_retryable_transcript_api_error(exc):
                raise TranscriptBackendError(str(exc)) from exc
            raise RetryableTranscriptError(str(exc)) from exc

        lines: list[str] = []
        for snippet in fetched:
            text = getattr(snippet, "text", None)
            if text is None and isinstance(snippet, dict):
                text = snippet.get("text", "")
            if text:
                lines.append(text)
        cleaned = clean_plain_text("\n".join(lines))
        if not cleaned:
            return TranscriptResult.unavailable(
                source=self.name,
                language=getattr(transcript, "language_code", options.language),
                error="empty transcript payload",
                backend_fingerprint=self.fingerprint(options),
            )
        return TranscriptResult.available(
            source=self.name,
            text=cleaned,
            language=getattr(transcript, "language_code", options.language),
            backend_fingerprint=self.fingerprint(options),
        )


class YtDlpSubtitleBackend:
    name = "yt_dlp"

    def _extract_info(self, item: ContentItem, options: TranscriptOptions):
        try:
            from yt_dlp import YoutubeDL
        except ImportError as exc:  # pragma: no cover - exercised in runtime environments without deps
            raise TranscriptBackendError("yt-dlp not installed") from exc

        ydl_options = {
            "skip_download": True,
            "noplaylist": True,
            "extract_flat": False,
            **_yt_dlp_request_options(options),
        }
        with YoutubeDL(ydl_options) as ydl:
            try:
                return ydl.extract_info(item.url, download=False)
            except Exception as exc:  # noqa: BLE001
                raise RetryableTranscriptError(str(exc)) from exc

    def fingerprint(self, options: TranscriptOptions) -> str:
        return f"{self.name}:{','.join(options.normalized_language_preferences())}"

    def fetch(self, item: ContentItem, options: TranscriptOptions) -> TranscriptResult:
        info = self._extract_info(item, options)
        preferences = options.normalized_language_preferences()
        manual = _select_track(info.get("subtitles") or {}, preferences)
        source = "yt_dlp_manual_subtitle"
        if manual is None:
            manual = _select_track(info.get("automatic_captions") or {}, preferences)
            source = "yt_dlp_auto_subtitle"
        if manual is None:
            return TranscriptResult.unavailable(
                source=self.name,
                language=options.language,
                error="no subtitles exposed by yt-dlp",
                backend_fingerprint=self.fingerprint(options),
            )

        language, track = manual
        request = urllib.request.Request(track["url"], headers=_browser_headers(options))
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = response.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            raise RetryableTranscriptError(str(exc)) from exc

        cleaned = clean_subtitle_payload(payload, track.get("ext", "vtt"))
        if not cleaned:
            return TranscriptResult.unavailable(
                source=source,
                language=language,
                error="subtitle payload was empty after cleaning",
                backend_fingerprint=self.fingerprint(options),
            )
        return TranscriptResult.available(
            source=source,
            text=cleaned,
            language=language,
            backend_fingerprint=self.fingerprint(options),
        )


class OpenAIAsrBackend:
    name = "openai_asr"

    def fingerprint(self, options: TranscriptOptions) -> str:
        return f"{self.name}:{options.asr_model}:{options.language}:mono16kmp3-v1"

    def _require_dependencies(self):
        try:
            import imageio_ffmpeg
            from openai import OpenAI
            from yt_dlp import YoutubeDL
        except ImportError as exc:  # pragma: no cover - exercised in runtime environments without deps
            raise TranscriptBackendError("OpenAI ASR dependencies not installed") from exc
        return imageio_ffmpeg, OpenAI, YoutubeDL

    def _download_audio(self, item: ContentItem, workdir: Path, YoutubeDL, options: TranscriptOptions) -> Path:
        outtmpl = str(workdir / f"{item.id}.%(ext)s")
        ydl_options = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            **_yt_dlp_request_options(options),
        }
        with YoutubeDL(ydl_options) as ydl:
            try:
                info = ydl.extract_info(item.url, download=True)
            except Exception as exc:  # noqa: BLE001
                raise RetryableTranscriptError(str(exc)) from exc
            path = Path(ydl.prepare_filename(info))
        if not path.exists():
            raise RetryableTranscriptError("yt-dlp did not produce an audio file")
        return path

    def _run_ffmpeg(self, command: list[str]) -> None:
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            raise TranscriptBackendError(exc.stderr.strip() or exc.stdout.strip() or "ffmpeg failed") from exc

    def _normalize_audio(self, input_path: Path, output_path: Path, ffmpeg_exe: str) -> None:
        self._run_ffmpeg(
            [
                ffmpeg_exe,
                "-y",
                "-i",
                str(input_path),
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-b:a",
                "48k",
                str(output_path),
            ]
        )

    def _chunk_audio(self, normalized_path: Path, ffmpeg_exe: str) -> list[Path]:
        if normalized_path.stat().st_size <= OPENAI_FILE_LIMIT_BYTES:
            return [normalized_path]
        chunk_pattern = normalized_path.with_name("chunk_%03d.mp3")
        self._run_ffmpeg(
            [
                ffmpeg_exe,
                "-y",
                "-i",
                str(normalized_path),
                "-f",
                "segment",
                "-segment_time",
                str(ASR_SEGMENT_SECONDS),
                "-c",
                "copy",
                str(chunk_pattern),
            ]
        )
        chunks = sorted(normalized_path.parent.glob("chunk_*.mp3"))
        if not chunks:
            raise TranscriptBackendError("audio chunking produced no files")
        return chunks

    def _transcribe_chunks(self, chunk_paths: list[Path], options: TranscriptOptions, OpenAI) -> str:
        client = OpenAI(api_key=options.openai_api_key)
        transcripts: list[str] = []
        for chunk_path in chunk_paths:
            with chunk_path.open("rb") as handle:
                try:
                    response = client.audio.transcriptions.create(
                        model=options.asr_model,
                        file=handle,
                        response_format="text",
                    )
                except Exception as exc:  # noqa: BLE001
                    raise RetryableTranscriptError(str(exc)) from exc
            text = getattr(response, "text", None)
            if text is None and isinstance(response, str):
                text = response
            transcripts.append(clean_plain_text(text or ""))
        return merge_transcript_chunks(transcripts)

    def fetch(self, item: ContentItem, options: TranscriptOptions) -> TranscriptResult:
        if not options.openai_api_key:
            return TranscriptResult.unavailable(
                source=self.name,
                language=options.language,
                error="missing OPENAI_API_KEY",
                backend_fingerprint=self.fingerprint(options),
            )
        imageio_ffmpeg, OpenAI, YoutubeDL = self._require_dependencies()
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        with tempfile.TemporaryDirectory(prefix=f"scrapling-asr-{item.id}-") as temp_dir:
            workdir = Path(temp_dir)
            downloaded = self._download_audio(item, workdir, YoutubeDL, options)
            normalized = workdir / "normalized.mp3"
            self._normalize_audio(downloaded, normalized, ffmpeg_exe)
            chunks = self._chunk_audio(normalized, ffmpeg_exe)
            merged = self._transcribe_chunks(chunks, options, OpenAI)

        if not merged:
            return TranscriptResult.unavailable(
                source=self.name,
                language=options.language,
                error="OpenAI ASR returned empty text",
                backend_fingerprint=self.fingerprint(options),
            )
        return TranscriptResult.available(
            source=self.name,
            text=merged,
            language=options.language,
            backend_fingerprint=self.fingerprint(options),
        )
