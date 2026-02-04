from __future__ import annotations

import asyncio
from typing import Iterable

from pricemonitor.scheduler.tasks import PollTask
from pricemonitor.storage.base import Storage


async def _run_task(task: PollTask, storage: Storage) -> None:
    while True:
        quote = await task.provider.fetch_quote(task.instrument)
        storage.append_quote(quote)
        await asyncio.sleep(task.interval_seconds)


async def run(tasks: Iterable[PollTask], storage: Storage) -> None:
    workers = [asyncio.create_task(_run_task(task, storage)) for task in tasks]
    if not workers:
        return
    await asyncio.gather(*workers)
