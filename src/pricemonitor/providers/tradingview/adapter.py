from __future__ import annotations

from typing import Iterable

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote
from pricemonitor.providers.base import ProviderCapabilities, ProviderError


class TradingViewProvider:
    """Adapter stub for TradingView metals pricing."""

    name = "tradingview"
    capabilities = ProviderCapabilities(supports_realtime=False, supports_historical=True)

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        raise ProviderError("TradingView adapter not implemented yet.")

    async def fetch_quotes(self, instruments: Iterable[Instrument]) -> list[Quote]:
        raise ProviderError("TradingView adapter not implemented yet.")
