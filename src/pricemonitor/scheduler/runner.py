from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Iterable

from pricemonitor.config.loader import ConfigError, load_app_config
from pricemonitor.models.instruments import Instrument
from pricemonitor.providers.base import ProviderError
from pricemonitor.providers.registry import build_providers
from pricemonitor.scheduler.tasks import PollTask
from pricemonitor.storage.base import Storage
from pricemonitor.storage.csv import CsvStorage


def _config_dir() -> Path:
    return Path(os.environ.get("PRICEMONITOR_CONFIG", "config"))


def _run_seconds() -> float | None:
    value = os.environ.get("PRICEMONITOR_RUN_SECONDS")
    if not value:
        return None
    try:
        seconds = float(value)
    except ValueError as exc:
        raise ConfigError(f"Invalid PRICEMONITOR_RUN_SECONDS: {value}") from exc
    return seconds if seconds > 0 else None


def build_instruments(config) -> dict[tuple[str, str], Instrument]:
    instruments: dict[tuple[str, str], Instrument] = {}
    for item in config.instruments:
        instruments[(item.symbol, item.provider)] = Instrument(
            symbol=item.symbol,
            asset_class=item.asset_class,
            exchange=item.exchange,
            base=item.base,
            quote=item.quote,
            name=item.name,
        )
    return instruments


def build_tasks(config_dir: Path) -> list[PollTask]:
    config = load_app_config(config_dir)
    providers = build_providers(config.providers)
    instruments = build_instruments(config)

    tasks: list[PollTask] = []
    for schedule in config.schedules:
        key = (schedule.symbol, schedule.provider)
        instrument = instruments.get(key)
        if instrument is None:
            raise ConfigError(f"Missing instrument for {schedule.provider}:{schedule.symbol}")
        provider = providers.get(schedule.provider)
        if provider is None:
            raise ConfigError(f"Missing provider configuration for {schedule.provider}")
        tasks.append(
            PollTask(
                instrument=instrument,
                provider=provider,
                interval_seconds=schedule.interval_seconds,
            )
        )
    return tasks


async def _run_task(task: PollTask, storage: Storage) -> None:
    while True:
        try:
            quote = await task.provider.fetch_quote(task.instrument)
            storage.append_quote(quote)
            print(
                f"[{quote.timestamp.isoformat()}] {quote.provider} {quote.instrument.symbol}={quote.price} {quote.currency}",
                flush=True,
            )
            await asyncio.sleep(task.interval_seconds)
        except ProviderError as exc:
            print(
                f"provider error ({task.provider.name}:{task.instrument.symbol}): {exc}",
                flush=True,
            )
            await asyncio.sleep(max(1.0, task.interval_seconds))
        except Exception as exc:  # pragma: no cover - safety net for long-running worker
            print(
                f"unexpected error ({task.provider.name}:{task.instrument.symbol}): {exc}",
                flush=True,
            )
            await asyncio.sleep(max(1.0, task.interval_seconds))


async def run(tasks: Iterable[PollTask], storage: Storage, run_seconds: float | None = None) -> None:
    workers = [asyncio.create_task(_run_task(task, storage)) for task in tasks]
    if not workers:
        return

    if run_seconds is None:
        await asyncio.gather(*workers)
        return

    try:
        await asyncio.sleep(run_seconds)
    finally:
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)


async def run_from_config(config_dir: Path, run_seconds: float | None = None) -> None:
    config = load_app_config(config_dir)
    storage = CsvStorage(Path(config.storage.root))
    tasks = build_tasks(config_dir)
    if not tasks:
        raise ConfigError("No polling tasks defined in schedules.yaml")
    await run(tasks, storage, run_seconds=run_seconds)


def run_main(config_dir: Path, run_seconds: float | None = None) -> None:
    asyncio.run(run_from_config(config_dir, run_seconds=run_seconds))


def main() -> None:
    run_main(_config_dir(), run_seconds=_run_seconds())


if __name__ == "__main__":
    main()
