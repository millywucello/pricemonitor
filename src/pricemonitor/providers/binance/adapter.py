from __future__ import annotations

import asyncio

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote
from pricemonitor.providers.base import ProviderCapabilities
from pricemonitor.providers.binance.client import BinanceClient
from pricemonitor.utils.time import utc_now


class BinanceProvider:
    """Adapter for Binance spot prices."""

    name = "binance"
    capabilities = ProviderCapabilities(supports_realtime=True, supports_historical=False)

    def __init__(self, client: BinanceClient | None = None, default_quote: str = "USDT") -> None:
        self.client = client or BinanceClient()
        self.default_quote = default_quote

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        price = await self.client.fetch_price(instrument.symbol)
        currency = instrument.quote or self.default_quote
        return Quote(
            instrument=instrument,
            price=price,
            timestamp=utc_now(),
            currency=currency,
            provider=self.name,
        )

    async def fetch_quotes(self, instruments: list[Instrument]) -> list[Quote]:
        if not instruments:
            return []
        tasks = [self.fetch_quote(instrument) for instrument in instruments]
        return list(await asyncio.gather(*tasks))
