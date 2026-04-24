from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ..models import TranscriptResult


class TranscriptCache:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = Path(base_dir) / "transcripts"

    def _path(self, video_id: str, backend_fingerprint: str) -> Path:
        digest = hashlib.sha256(backend_fingerprint.encode("utf-8")).hexdigest()[:16]
        return self.base_dir / video_id / f"{digest}.json"

    def load(self, video_id: str, backend_fingerprint: str) -> TranscriptResult | None:
        path = self._path(video_id, backend_fingerprint)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        return TranscriptResult(
            status=payload["status"],
            source=payload.get("source", ""),
            language=payload.get("language", ""),
            text=payload.get("text", ""),
            error=payload.get("error", ""),
            backend_fingerprint=payload.get("backend_fingerprint", backend_fingerprint),
            cached=True,
            characters=payload.get("characters", 0),
        )

    def save(self, video_id: str, result: TranscriptResult) -> Path:
        path = self._path(video_id, result.backend_fingerprint)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "status": result.status,
                    "source": result.source,
                    "language": result.language,
                    "text": result.text,
                    "error": result.error,
                    "backend_fingerprint": result.backend_fingerprint,
                    "characters": result.characters,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return path
