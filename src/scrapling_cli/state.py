from __future__ import annotations

import json
import logging
from datetime import date, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        logger.warning("state.read_failed path=%s error=%s", path, exc)
        return {}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def get_last_run(state: dict, channel_key: str, days_back: int) -> date:
    key = f"last_run_{channel_key}"
    raw = state.get(key)
    if raw:
        try:
            return date.fromisoformat(raw)
        except ValueError:
            logger.warning("state.invalid_date key=%s value=%s", key, raw)
    return date.today() - timedelta(days=days_back)
