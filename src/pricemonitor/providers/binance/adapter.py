from __future__ import annotations

from typing import Iterable

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote
from pricemonitor.providers.base import ProviderCapabilities, ProviderError


class BinanceProvider:
    """Adapter stub for Binance spot prices."""

    name = "binance"
    capabilities = ProviderCapabilities(supports_realtime=True, supports_historical=False)

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        raise ProviderError("Binance adapter not implemented yet.")

    async def fetch_quotes(self, instruments: Iterable[Instrument]) -> list[Quote]:
        raise ProviderError("Binance adapter not implemented yet.")
