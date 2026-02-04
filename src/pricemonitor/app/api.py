from __future__ import annotations

from typing import Any

from pricemonitor.storage.base import Storage

try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover - optional dependency
    FastAPI = None


def create_app(storage: Storage | None = None) -> Any:
    if FastAPI is None:
        raise RuntimeError("FastAPI is required to create the web API.")

    app = FastAPI(title="Price Monitor API")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/prices/latest")
    def latest(symbol: str) -> dict[str, Any]:
        if storage is None:
            return {"symbol": symbol, "error": "storage not configured"}
        from pricemonitor.models.instruments import AssetClass, Instrument

        instrument = Instrument(symbol=symbol, asset_class=AssetClass.CRYPTO)
        quote = storage.latest(instrument)
        if quote is None:
            return {"symbol": symbol, "error": "no data"}
        return {
            "symbol": quote.instrument.symbol,
            "price": quote.price,
            "timestamp": quote.timestamp.isoformat(),
            "currency": quote.currency,
            "provider": quote.provider,
        }

    return app
