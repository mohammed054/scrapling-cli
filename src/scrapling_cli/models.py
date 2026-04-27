from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Literal, Optional

TranscriptStatus = Literal["available", "unavailable", "skipped"]


@dataclass(slots=True)
class ScoreComponents:
    rank_by: str = "weighted"
    norm_views: float = 0.0
    norm_likes: float = 0.0
    norm_comments: float = 0.0
    engagement_rate: float = 0.0
    norm_engagement: float = 0.0


@dataclass(slots=True)
class TranscriptResult:
    status: TranscriptStatus
    source: str = ""
    language: str = ""
    text: str = ""
    error: str = ""
    backend_fingerprint: str = ""
    cached: bool = False
    characters: int = 0

    def __post_init__(self) -> None:
        if self.text and not self.characters:
            self.characters = len(self.text)

    @classmethod
    def available(
        cls,
        *,
        source: str,
        text: str,
        language: str = "",
        backend_fingerprint: str = "",
        cached: bool = False,
    ) -> "TranscriptResult":
        return cls(
            status="available",
            source=source,
            language=language,
            text=text.strip(),
            backend_fingerprint=backend_fingerprint,
            cached=cached,
        )

    @classmethod
    def unavailable(
        cls,
        *,
        source: str = "",
        error: str = "",
        language: str = "",
        backend_fingerprint: str = "",
        cached: bool = False,
    ) -> "TranscriptResult":
        return cls(
            status="unavailable",
            source=source,
            language=language,
            error=error.strip(),
            backend_fingerprint=backend_fingerprint,
            cached=cached,
        )

    @classmethod
    def skipped(
        cls,
        reason: str = "transcripts_disabled",
        *,
        source: str = "skipped",
        language: str = "",
    ) -> "TranscriptResult":
        return cls(status="skipped", source=source, language=language, error=reason)


@dataclass(slots=True)
class ContentItem:
    id: str
    title: str
    url: str
    type: str = "video"
    views: int = 0
    likes: int = 0
    comments: int = 0
    date: Optional[date] = None
    duration: int = 0
    description: str = ""
    channel: str = ""
    channel_url: str = ""
    subscribers: int = 0
    thumbnail: str = ""
    tags: list[str] = field(default_factory=list)
    category: str = ""
    language: str = ""
    age_limit: int = 0
    chapters: list[dict] = field(default_factory=list)
    top_comments: list[dict] = field(default_factory=list)
    transcript: TranscriptResult = field(default_factory=lambda: TranscriptResult.skipped("not_requested"))
    score: float = 0.0
    score_components: ScoreComponents = field(default_factory=ScoreComponents)
    like_ratio: float = 0.0
    comment_ratio: float = 0.0
    published_relative: str = ""
    upload_date: str = ""
    source_tab: str = ""

    def __post_init__(self) -> None:
        self.refresh_metrics()

    def refresh_metrics(self) -> None:
        base_views = max(self.views, 1)
        self.like_ratio = round(self.likes / base_views * 100, 4)
        self.comment_ratio = round(self.comments / base_views * 100, 4)


@dataclass(slots=True)
class TranscriptOptions:
    enabled: bool = False
    language: str = "en"
    cache_dir: Path = Path(".cache/scrapling-cli")
    workers: int = 4
    allow_hosted_asr: Optional[bool] = None
    asr_model: str = "gpt-4o-mini-transcribe"
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    def hosted_asr_enabled(self) -> bool:
        if self.allow_hosted_asr is None:
            return bool(self.openai_api_key)
        return bool(self.allow_hosted_asr and self.openai_api_key)

    def normalized_language_preferences(self) -> list[str]:
        base = (self.language or "en").strip()
        values = [base]
        if base.startswith("en"):
            values.extend(["en-US", "en-GB", "en"])
        elif "-" in base:
            values.append(base.split("-", 1)[0])
        deduped: list[str] = []
        for value in values:
            if value and value not in deduped:
                deduped.append(value)
        return deduped or ["en"]


@dataclass(slots=True)
class ChannelRunConfig:
    channel: str
    top_percent: float = 15.0
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    rank_by: str = "weighted"
    recency_decay: bool = False
    clamp_outliers: bool = False
    no_shorts: bool = False
    no_videos: bool = False
    no_enrich: bool = False
    output_dir: Path = Path("output")
    export_csv: bool = False
    no_report: bool = False
    dry_run: bool = False
    verbose: bool = False
    log_file: Optional[Path] = None
    transcript_options: TranscriptOptions = field(default_factory=TranscriptOptions)


@dataclass(slots=True)
class ChannelRunResult:
    channel_name: str
    channel_slug: str
    videos: list[ContentItem]
    shorts: list[ContentItem]
    top_videos: list[ContentItem]
    top_shorts: list[ContentItem]
    scraped_item_count: int = 0
    candidate_item_count: int = 0
    written_files: list[Path] = field(default_factory=list)
    report_path: Optional[Path] = None
    csv_paths: list[Path] = field(default_factory=list)
    output_root: Optional[Path] = None


@dataclass(slots=True)
class FetchNewRunConfig:
    channels: list[str]
    days_back: int = 7
    output_dir: Path = Path("output_new")
    state_file: Path = Path("state.json")
    force_from: Optional[date] = None
    verbose: bool = False
    log_file: Optional[Path] = None
    transcript_options: TranscriptOptions = field(default_factory=TranscriptOptions)


@dataclass(slots=True)
class IncrementalChannelResult:
    channel: str
    channel_name: str
    channel_slug: str
    from_date: date
    items: list[ContentItem] = field(default_factory=list)
    written_files: list[Path] = field(default_factory=list)


@dataclass(slots=True)
class FetchNewRunResult:
    channel_results: list[IncrementalChannelResult]

    @property
    def total_written(self) -> int:
        return sum(len(result.written_files) for result in self.channel_results)
