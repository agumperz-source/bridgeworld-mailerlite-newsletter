"""Run the Bridge World package validators.

Usage:
    python -m validators.run_all --package .
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tbw_converter.validation_core import main


if __name__ == "__main__":
    raise SystemExit(main())
