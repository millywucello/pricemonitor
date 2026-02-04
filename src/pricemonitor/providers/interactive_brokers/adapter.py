from __future__ import annotations

from typing import Iterable

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote
from pricemonitor.providers.base import ProviderCapabilities, ProviderError


class InteractiveBrokersProvider:
    """Adapter stub for Interactive Brokers market data."""

    name = "interactive_brokers"
    capabilities = ProviderCapabilities(supports_realtime=True, supports_historical=True)

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        raise ProviderError("Interactive Brokers adapter not implemented yet.")

    async def fetch_quotes(self, instruments: Iterable[Instrument]) -> list[Quote]:
        raise ProviderError("Interactive Brokers adapter not implemented yet.")
