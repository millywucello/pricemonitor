from __future__ import annotations

from typing import Iterable

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote
from pricemonitor.providers.base import HistoryQuery, ProviderCapabilities, ProviderError


class TradingViewProvider:
    """Adapter stub for TradingView metals pricing."""

    name = "tradingview"
    capabilities = ProviderCapabilities(supports_realtime=False, supports_historical=True)

    async def get_latest_price(self, symbol: str) -> Quote:
        raise ProviderError(f"TradingView adapter not implemented yet: {symbol}")

    async def get_history(self, query: HistoryQuery) -> list[Quote]:
        raise ProviderError(f"TradingView history not implemented yet: {query.symbol}")

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        raise ProviderError("TradingView adapter not implemented yet.")

    async def fetch_quotes(self, instruments: Iterable[Instrument]) -> list[Quote]:
        raise ProviderError("TradingView adapter not implemented yet.")
