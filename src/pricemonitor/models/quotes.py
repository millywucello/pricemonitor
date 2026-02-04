from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .instruments import Instrument


@dataclass(frozen=True)
class Quote:
    instrument: Instrument
    price: float
    timestamp: datetime
    currency: str
    provider: str
    extra: dict[str, Any] = field(default_factory=dict)
