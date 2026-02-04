from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote


class ProviderError(RuntimeError):
    """Base error for provider failures."""


@dataclass(frozen=True)
class ProviderCapabilities:
    supports_realtime: bool = True
    supports_historical: bool = False


class Provider(Protocol):
    name: str
    capabilities: ProviderCapabilities

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        """Fetch a single quote for an instrument."""

    async def fetch_quotes(self, instruments: Iterable[Instrument]) -> list[Quote]:
        """Fetch multiple quotes in a single request when supported."""
