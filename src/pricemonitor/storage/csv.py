from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from pricemonitor.models.instruments import Instrument
from pricemonitor.models.quotes import Quote
from pricemonitor.storage.base import Storage


class CsvStorage(Storage):
    """Append-only CSV storage, partitioned by instrument symbol."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def append_quote(self, quote: Quote) -> None:
        path = self._path_for(quote.instrument)
        write_header = not path.exists() or path.stat().st_size == 0
        with path.open("a", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            if write_header:
                writer.writerow(self._header())
            writer.writerow(self._row(quote))

    def append_quotes(self, quotes: list[Quote]) -> None:
        for quote in quotes:
            self.append_quote(quote)

    def latest(self, instrument: Instrument) -> Quote | None:
        path = self._path_for(instrument)
        if not path.exists():
            return None
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if len(rows) <= 1:
            return None
        return self._parse_row(rows[-1], instrument)

    def history(self, instrument: Instrument, limit: int | None = None) -> list[Quote]:
        path = self._path_for(instrument)
        if not path.exists():
            return []
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        data_rows = rows[1:]
        if limit:
            data_rows = data_rows[-limit:]
        return [self._parse_row(row, instrument) for row in data_rows]

    def _path_for(self, instrument: Instrument) -> Path:
        filename = instrument.symbol.lower().replace("/", "-")
        return self.root / f"{filename}.csv"

    @staticmethod
    def _header() -> list[str]:
        return [
            "timestamp",
            "provider",
            "symbol",
            "display_symbol",
            "price",
            "currency",
        ]

    @staticmethod
    def _row(quote: Quote) -> list[str]:
        return [
            quote.timestamp.isoformat(),
            quote.provider,
            quote.instrument.symbol,
            quote.instrument.display_symbol,
            f"{quote.price:.10f}",
            quote.currency,
        ]

    @staticmethod
    def _parse_row(row: list[str], instrument: Instrument) -> Quote:
        timestamp = datetime.fromisoformat(row[0])
        provider = row[1]
        price = float(row[4])
        currency = row[5]
        return Quote(
            instrument=instrument,
            price=price,
            timestamp=timestamp,
            currency=currency,
            provider=provider,
        )
