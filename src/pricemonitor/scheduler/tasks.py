from __future__ import annotations

from dataclasses import dataclass

from pricemonitor.models.instruments import Instrument
from pricemonitor.providers.base import Provider


@dataclass(frozen=True)
class PollTask:
    instrument: Instrument
    provider: Provider
    interval_seconds: float
