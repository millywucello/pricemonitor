from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AssetClass(str, Enum):
    CRYPTO = "crypto"
    METAL = "metal"
    EQUITY = "equity"
    FX = "fx"


@dataclass(frozen=True)
class Instrument:
    """Canonical representation of a tradable instrument."""

    symbol: str
    asset_class: AssetClass
    exchange: str | None = None
    base: str | None = None
    quote: str | None = None
    name: str | None = None

    @property
    def display_symbol(self) -> str:
        if self.base and self.quote:
            return f"{self.base}/{self.quote}"
        return self.symbol
