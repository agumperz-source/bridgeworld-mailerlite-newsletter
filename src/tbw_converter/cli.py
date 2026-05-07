"""Command-line entrypoint for the Bridge World newsletter tooling."""

from __future__ import annotations

from .validation_core import main


if __name__ == "__main__":
    raise SystemExit(main())
