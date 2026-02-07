from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pricemonitor.config.loader import ConfigError
from pricemonitor.providers.base import ProviderError
from pricemonitor.providers.registry import build_provider_from_config

try:
    from fastapi import FastAPI, HTTPException
except ImportError:  # pragma: no cover - optional dependency
    FastAPI = None


def _config_dir() -> Path:
    return Path(os.environ.get("PRICEMONITOR_CONFIG", "config"))


def create_app() -> Any:
    if FastAPI is None:
        raise RuntimeError("FastAPI is required to create the web API.")

    app = FastAPI(title="Price Monitor API")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/prices/latest")
    async def latest(provider: str, symbol: str) -> dict[str, Any]:
        try:
            provider_instance = build_provider_from_config(_config_dir(), provider)
        except ConfigError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        try:
            quote = await provider_instance.get_latest_price(symbol)
        except ProviderError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc
        finally:
            close = getattr(provider_instance, "close", None)
            if close is not None:
                await close()

        return {
            "symbol": quote.instrument.symbol,
            "price": quote.price,
            "timestamp": quote.timestamp.isoformat(),
            "currency": quote.currency,
            "provider": quote.provider,
        }

    return app
