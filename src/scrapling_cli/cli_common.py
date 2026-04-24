from __future__ import annotations

from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path

from .models import TranscriptOptions


def parse_date_arg(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


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
    group.add_argument("--workers", type=int, default=4, help="Transcript worker count (default: 4)")
    hosted = group.add_mutually_exclusive_group()
    hosted.add_argument(
        "--allow-hosted-asr",
        dest="allow_hosted_asr",
        action="store_true",
        help="Allow OpenAI ASR fallback when OPENAI_API_KEY is set",
    )
    hosted.add_argument(
        "--no-hosted-asr",
        dest="allow_hosted_asr",
        action="store_false",
        help="Disable OpenAI ASR fallback even if OPENAI_API_KEY is set",
    )
    parser.set_defaults(allow_hosted_asr=None)
    group.add_argument(
        "--asr-model",
        default="gpt-4o-mini-transcribe",
        help="OpenAI transcription model for hosted ASR fallback",
    )


def build_transcript_options(args: Namespace) -> TranscriptOptions:
    return TranscriptOptions(
        enabled=bool(getattr(args, "transcripts", False)),
        language=args.transcript_language,
        cache_dir=Path(args.cache_dir),
        workers=max(1, args.workers),
        allow_hosted_asr=args.allow_hosted_asr,
        asr_model=args.asr_model,
    )
