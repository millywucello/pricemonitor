from __future__ import annotations

import httpx


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
        response = await self._client.get("/api/v3/ticker/price", params={"symbol": symbol})
        response.raise_for_status()
        data = response.json()
        return float(data["price"])

    async def close(self) -> None:
        await self._client.aclose()
