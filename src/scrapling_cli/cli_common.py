from __future__ import annotations

import os
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path

from .models import TranscriptOptions


def load_env_file(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE pairs without overriding the process environment."""
    if not path.exists():
        return
    import os

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        value = value.strip().strip('"').strip("'")
        os.environ[key] = value


def parse_date_arg(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def describe_hosted_asr(options: TranscriptOptions) -> str:
    if options.allow_hosted_asr is False:
        return "disabled"
    providers = []
    if options.openai_api_key:
        providers.append("openai")
    if options.openrouter_api_key:
        providers.append("openrouter")
    return ", ".join(providers) if providers else "off"


def describe_cookie_source(options: TranscriptOptions) -> str:
    if options.cookies_from_browser:
        return f"browser:{options.cookies_from_browser}"
    if options.cookies_file:
        return "file"
    return "off"


def _env_first(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def add_transcript_arguments(parser: ArgumentParser) -> None:
    group = parser.add_argument_group("Transcripts")
    group.add_argument("--transcripts", action="store_true", help="Resolve transcripts for selected items")
    group.add_argument(
        "--transcript-language",
        default="en",
        help="Preferred transcript language code (default: en)",
    )
    group.add_argument(
        "--cache-dir",
        default=".cache/scrapling-cli",
        help="Repo-local cache directory for transcripts and ASR artifacts",
    )
    group.add_argument("--workers", type=int, default=1, help="Transcript worker count (default: 1)")
    group.add_argument(
        "--transcript-delay",
        type=float,
        default=4.0,
        help="Minimum delay in seconds between transcript requests across workers (default: 4.0)",
    )
    group.add_argument(
        "--transcript-retries",
        type=int,
        default=4,
        help="Retry attempts per transcript backend for retryable failures (default: 4)",
    )
    group.add_argument(
        "--transcript-rate-limit-cooldown",
        type=float,
        default=300.0,
        help="Base cooldown in seconds after YouTube 429/bot-block responses (default: 300)",
    )
    group.add_argument(
        "--transcript-rate-limit-cap",
        type=float,
        default=3600.0,
        help="Maximum cooldown in seconds after repeated YouTube 429/bot-block responses (default: 3600)",
    )
    group.add_argument(
        "--allow-missing-transcripts",
        dest="require_transcript_success",
        action="store_false",
        help="Finish the run even when some transcripts remain unavailable",
    )
    hosted = group.add_mutually_exclusive_group()
    hosted.add_argument(
        "--allow-hosted-asr",
        dest="allow_hosted_asr",
        action="store_true",
        help="Allow hosted ASR fallback when OPENAI_API_KEY or OPENROUTER_API_KEY is set",
    )
    hosted.add_argument(
        "--no-hosted-asr",
        dest="allow_hosted_asr",
        action="store_false",
        help="Disable hosted ASR fallback even if an ASR API key is set",
    )
    parser.set_defaults(allow_hosted_asr=None, require_transcript_success=True)
    group.add_argument(
        "--asr-model",
        default="gpt-4o-mini-transcribe",
        help="OpenAI transcription model for hosted ASR fallback",
    )
    group.add_argument(
        "--openrouter-asr-model",
        default="openai/whisper-large-v3",
        help="OpenRouter STT model slug for hosted ASR fallback",
    )
    group.add_argument(
        "--cookies-from-browser",
        default="",
        metavar="BROWSER[:PROFILE]",
        help="Let yt-dlp load YouTube cookies from a browser, for example chrome or edge:Default",
    )
    group.add_argument(
        "--cookies",
        default="",
        metavar="FILE",
        help="Path to a Netscape cookies.txt file for yt-dlp YouTube requests",
    )


def build_transcript_options(args: Namespace) -> TranscriptOptions:
    load_env_file()
    cookies_from_browser = (
        (args.cookies_from_browser or "").strip()
        or _env_first("YTDLP_COOKIES_FROM_BROWSER", "SCRAPLING_COOKIES_FROM_BROWSER")
    )
    cookies_file = (args.cookies or "").strip() or _env_first("YTDLP_COOKIES", "SCRAPLING_COOKIES")
    return TranscriptOptions(
        enabled=bool(getattr(args, "transcripts", False)),
        language=args.transcript_language,
        cache_dir=Path(args.cache_dir),
        workers=max(1, args.workers),
        request_delay_seconds=max(0.0, args.transcript_delay),
        retry_attempts=max(1, args.transcript_retries),
        rate_limit_cooldown_seconds=max(1.0, args.transcript_rate_limit_cooldown),
        rate_limit_cooldown_cap_seconds=max(1.0, args.transcript_rate_limit_cap),
        require_success=bool(args.require_transcript_success),
        allow_hosted_asr=args.allow_hosted_asr,
        asr_model=args.asr_model,
        openrouter_asr_model=args.openrouter_asr_model,
        cookies_from_browser=cookies_from_browser,
        cookies_file=Path(cookies_file) if cookies_file else None,
    )
