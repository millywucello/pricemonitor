from __future__ import annotations

from typing import Iterable, Protocol

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote


class Storage(Protocol):
    """Persistence interface for quotes."""

    def append_quote(self, quote: Quote) -> None:
        """Persist a single quote."""

    def append_quotes(self, quotes: Iterable[Quote]) -> None:
        """Persist multiple quotes."""

    def latest(self, instrument: Instrument) -> Quote | None:
        """Return the latest quote for an instrument."""

    def history(self, instrument: Instrument, limit: int | None = None) -> list[Quote]:
        """Return recent quotes for an instrument."""
