from __future__ import annotations

import httpx

from pricemonitor.providers.base import ProviderError


class BinanceClient:
    """Low-level HTTP client for Binance public endpoints."""

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        base_url: str = "https://api.binance.com",
        timeout: float = 10.0,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def fetch_price(self, symbol: str) -> float:
        try:
            response = await self._client.get("/api/v3/ticker/price", params={"symbol": symbol})
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"Binance HTTP error for {symbol}: {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise ProviderError(f"Binance network error for {symbol}: {exc}") from exc

        data = response.json()
        price = data.get("price")
        if price is None:
            raise ProviderError(f"Binance response missing price for {symbol}: {data}")
        try:
            return float(price)
        except (TypeError, ValueError) as exc:
            raise ProviderError(f"Binance price parse failed for {symbol}: {price}") from exc

    async def close(self) -> None:
        await self._client.aclose()
