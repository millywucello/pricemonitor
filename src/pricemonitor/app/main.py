from __future__ import annotations

import os
from pathlib import Path

from pricemonitor.app.api import create_app
from pricemonitor.app.deps import load_storage


def _config_dir() -> Path:
    return Path(os.environ.get("PRICEMONITOR_CONFIG", "config"))


def build_app():
    storage = load_storage(_config_dir())
    return create_app(storage)


app = build_app()
