from __future__ import annotations

from pathlib import Path

from pricemonitor.config.loader import ConfigError, load_app_config
from pricemonitor.config.models import ProviderConfig
from pricemonitor.providers.base import Provider
from pricemonitor.providers.binance.adapter import BinanceProvider
from pricemonitor.providers.binance.client import BinanceClient
from pricemonitor.providers.interactive_brokers.adapter import InteractiveBrokersProvider
from pricemonitor.providers.tradingview.adapter import TradingViewProvider


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
    if config.kind == "tradingview":
        return TradingViewProvider()
    if config.kind == "interactive_brokers":
        return InteractiveBrokersProvider()
    raise ProviderRegistryError(f"Provider kind '{config.kind}' is not implemented yet.")


def build_providers(configs: dict[str, ProviderConfig]) -> dict[str, Provider]:
    return {name: build_provider(cfg) for name, cfg in configs.items()}


def build_provider_from_config(config_dir: Path, name: str) -> Provider:
    app_config = load_app_config(config_dir)
    provider_config = app_config.providers.get(name)
    if provider_config is None:
        raise ConfigError(f"Unknown provider: {name}")
    try:
        return build_provider(provider_config)
    except ProviderRegistryError as exc:
        raise ConfigError(f"Failed to construct provider {name}: {exc}") from exc
