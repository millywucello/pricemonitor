from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Protocol

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote


class ProviderError(RuntimeError):
    """Base error for provider failures."""


@dataclass(frozen=True)
class ProviderCapabilities:
    supports_realtime: bool = True
    supports_historical: bool = False


@dataclass(frozen=True)
class HistoryQuery:
    symbol: str
    interval: str
    start: datetime | None = None
    end: datetime | None = None


class Provider(Protocol):
    name: str
    capabilities: ProviderCapabilities

    async def get_latest_price(self, symbol: str) -> Quote:
        """Fetch the latest quote for a provider-native symbol."""

    async def get_history(self, query: HistoryQuery) -> list[Quote]:
        """Fetch historical quotes for a provider-native symbol."""

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        """Fetch a single quote for an instrument."""

    async def fetch_quotes(self, instruments: Iterable[Instrument]) -> list[Quote]:
        """Fetch multiple quotes in a single request when supported."""
