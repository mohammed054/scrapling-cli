#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PACKAGE_DIR = SRC / "scrapling_cli"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
__path__ = [str(PACKAGE_DIR)]
__version__ = "0.2.0"


if __name__ == "__main__":
    from scrapling_cli.cli import main

    raise SystemExit(main())
