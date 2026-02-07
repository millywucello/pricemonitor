from __future__ import annotations

import asyncio

from pricemonitor.models.instruments import AssetClass, Instrument
from pricemonitor.models.quotes import Quote
from pricemonitor.providers.base import HistoryQuery, ProviderCapabilities, ProviderError
from pricemonitor.providers.binance.client import BinanceClient
from pricemonitor.utils.time import utc_now


class BinanceProvider:
    """Adapter for Binance spot prices."""

    name = "binance"
    capabilities = ProviderCapabilities(supports_realtime=True, supports_historical=False)

    def __init__(self, client: BinanceClient | None = None, default_quote: str = "USDT") -> None:
        self.client = client or BinanceClient()
        self.default_quote = default_quote

    async def get_latest_price(self, symbol: str) -> Quote:
        price = await self.client.fetch_price(symbol)
        instrument = Instrument(
            symbol=symbol,
            asset_class=AssetClass.CRYPTO,
            quote=self.default_quote,
        )
        return Quote(
            instrument=instrument,
            price=price,
            timestamp=utc_now(),
            currency=self.default_quote,
            provider=self.name,
        )

    async def get_history(self, query: HistoryQuery) -> list[Quote]:
        raise ProviderError(f"Binance history not implemented yet: {query.symbol}")

    async def fetch_quote(self, instrument: Instrument) -> Quote:
        quote = await self.get_latest_price(instrument.symbol)
        if instrument.quote and instrument.quote != quote.currency:
            quote = Quote(
                instrument=quote.instrument,
                price=quote.price,
                timestamp=quote.timestamp,
                currency=instrument.quote,
                provider=quote.provider,
            )
        return Quote(
            instrument=instrument,
            price=quote.price,
            timestamp=quote.timestamp,
            currency=quote.currency,
            provider=quote.provider,
        )

    async def fetch_quotes(self, instruments: list[Instrument]) -> list[Quote]:
        if not instruments:
            return []
        tasks = [self.fetch_quote(instrument) for instrument in instruments]
        return list(await asyncio.gather(*tasks))

    async def close(self) -> None:
        await self.client.close()
