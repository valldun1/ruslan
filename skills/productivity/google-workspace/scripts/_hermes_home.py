"""Resolve RUSLAN_HOME for standalone skill scripts.

Skill scripts may run outside the Ruslan process (e.g. system Python,
nix env, CI) where ``ruslan_constants`` is not importable.  This module
provides the same ``get_ruslan_home()`` and ``display_ruslan_home()``
contracts as ``ruslan_constants`` without requiring it on ``sys.path``.

When ``ruslan_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``ruslan_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``RUSLAN_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from ruslan_constants import display_ruslan_home as display_ruslan_home
    from ruslan_constants import get_ruslan_home as get_ruslan_home
except (ModuleNotFoundError, ImportError):

    def get_ruslan_home() -> Path:
        """Return the Ruslan home directory (default: ~/.ruslan).

        Mirrors ``ruslan_constants.get_ruslan_home()``."""
        val = os.environ.get("RUSLAN_HOME", "").strip()
        return Path(val) if val else Path.home() / ".ruslan"

    def display_ruslan_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``ruslan_constants.display_ruslan_home()``."""
        home = get_ruslan_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
