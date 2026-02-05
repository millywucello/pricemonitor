from __future__ import annotations

import asyncio
import os
from pathlib import Path

from pricemonitor.config.loader import ConfigError, load_app_config
from pricemonitor.models.instruments import Instrument
from pricemonitor.providers.registry import build_providers
from pricemonitor.scheduler.runner import run
from pricemonitor.scheduler.tasks import PollTask
from pricemonitor.storage.csv import CsvStorage


def build_instruments(config) -> dict[tuple[str, str], Instrument]:
    instruments = {}
    for item in config.instruments:
        key = (item.symbol, item.provider)
        instruments[key] = Instrument(
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


async def run_from_config(config_dir: Path) -> None:
    config = load_app_config(config_dir)
    storage = CsvStorage(Path(config.storage.root))
    tasks = build_tasks(config_dir)
    if not tasks:
        raise ConfigError("No polling tasks defined in schedules.yaml")
    await run(tasks, storage)


def run_main(config_dir: Path) -> None:
    asyncio.run(run_from_config(config_dir))


def _config_dir() -> Path:
    return Path(os.environ.get("PRICEMONITOR_CONFIG", "config"))


def main() -> None:
    run_main(_config_dir())
