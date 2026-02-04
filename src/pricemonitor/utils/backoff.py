from __future__ import annotations

import random


def exponential_backoff(
    attempt: int,
    base: float = 0.5,
    cap: float = 60.0,
    jitter: float = 0.1,
) -> float:
    """Return a backoff delay with jitter."""

    delay = min(cap, base * (2 ** max(attempt, 0)))
    return delay * (1 + random.uniform(-jitter, jitter))
