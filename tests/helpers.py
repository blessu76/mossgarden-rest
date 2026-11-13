"""Shared test setup: puts scripts/ on sys.path and exposes REPO."""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))


def isolated_env(home, **extra):
    """Environment for ops scripts in tests: HOME is a throw-away dir, so nothing falls back to the real ~/.ipe, ~/Developer/mossgarden-rest or ~/Library/LaunchAgents."""
    import os
    env = {**os.environ, "HOME": str(home), "PYTHONDONTWRITEBYTECODE": "1"}
    for k in ("MOSSGARDEN_PUBLISH_DIR", "MOSSGARDEN_SLOT_FILE", "MOSSGARDEN_NOW", "MOSSGARDEN_PUBLISH_CMD", "MOSSGARDEN_SEED", "MOSSGARDEN_TODAY"):
        env.pop(k, None)
    env.update(extra)
    return env
