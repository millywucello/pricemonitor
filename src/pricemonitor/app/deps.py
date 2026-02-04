from __future__ import annotations

from pathlib import Path

from pricemonitor.config.loader import load_app_config
from pricemonitor.storage.csv import CsvStorage


def load_storage(config_dir: Path) -> CsvStorage:
    config = load_app_config(config_dir)
    return CsvStorage(Path(config.storage.root))
