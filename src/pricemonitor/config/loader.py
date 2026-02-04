from __future__ import annotations

from pathlib import Path
from typing import Any

from pricemonitor.config.models import (
    AppConfig,
    InstrumentConfig,
    ProviderConfig,
    ScheduleConfig,
    StorageConfig,
)
from pricemonitor.models.instruments import AssetClass

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


class ConfigError(RuntimeError):
    """Raised when configuration cannot be loaded."""


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise ConfigError("PyYAML is required to load YAML config files.")
    if not path.exists():
        raise ConfigError(f"Missing config file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"Invalid config format in {path}")
    return data


def load_app_config(config_dir: Path) -> AppConfig:
    sources = load_yaml(config_dir / "sources.yaml")
    schedules = load_yaml(config_dir / "schedules.yaml")
    storage = load_yaml(config_dir / "storage.yaml")

    providers = {
        name: ProviderConfig(name=name, kind=details.get("kind", name), settings=details.get("settings", {}))
        for name, details in (sources.get("providers") or {}).items()
    }

    instruments = [
        InstrumentConfig(
            symbol=item["symbol"],
            asset_class=AssetClass(item["asset_class"]),
            provider=item["provider"],
            base=item.get("base"),
            quote=item.get("quote"),
            exchange=item.get("exchange"),
            name=item.get("name"),
        )
        for item in (sources.get("instruments") or [])
    ]

    schedule_items = [
        ScheduleConfig(
            symbol=item["symbol"],
            provider=item["provider"],
            interval_seconds=int(item["interval_seconds"]),
        )
        for item in (schedules.get("schedules") or [])
    ]

    storage_cfg = storage.get("storage") or {}
    storage_config = StorageConfig(
        backend=storage_cfg.get("backend", "csv"),
        root=storage_cfg.get("root", "data"),
    )

    return AppConfig(
        providers=providers,
        instruments=instruments,
        schedules=schedule_items,
        storage=storage_config,
    )
