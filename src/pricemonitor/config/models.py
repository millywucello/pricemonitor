from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pricemonitor.models.instruments import AssetClass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    kind: str
    settings: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InstrumentConfig:
    symbol: str
    asset_class: AssetClass
    provider: str
    base: str | None = None
    quote: str | None = None
    exchange: str | None = None
    name: str | None = None


@dataclass(frozen=True)
class ScheduleConfig:
    symbol: str
    provider: str
    interval_seconds: int


@dataclass(frozen=True)
class StorageConfig:
    backend: str
    root: str


@dataclass(frozen=True)
class AppConfig:
    providers: dict[str, ProviderConfig]
    instruments: list[InstrumentConfig]
    schedules: list[ScheduleConfig]
    storage: StorageConfig
