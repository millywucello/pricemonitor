from __future__ import annotations

from pricemonitor.config.models import ProviderConfig
from pricemonitor.providers.base import Provider
from pricemonitor.providers.binance.adapter import BinanceProvider
from pricemonitor.providers.binance.client import BinanceClient


class ProviderRegistryError(RuntimeError):
    """Raised when a provider cannot be constructed."""


def build_provider(config: ProviderConfig) -> Provider:
    if config.kind == "binance":
        settings = config.settings or {}
        client = BinanceClient(
            api_key=settings.get("api_key"),
            api_secret=settings.get("api_secret"),
        )
        return BinanceProvider(client=client, default_quote=settings.get("default_quote", "USDT"))
    raise ProviderRegistryError(f"Provider kind '{config.kind}' is not implemented yet.")


def build_providers(configs: dict[str, ProviderConfig]) -> dict[str, Provider]:
    return {name: build_provider(cfg) for name, cfg in configs.items()}
