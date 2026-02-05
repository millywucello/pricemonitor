# Price Monitor

A modular Python service for polling prices from multiple finance platforms, normalizing data, and storing it for analysis. The design keeps provider adapters isolated and lets you configure refresh intervals per instrument.

## Goals
- Fetch crypto, metals, and equities from multiple providers.
- Configure per-instrument refresh rates (e.g., BTC every second, US stocks every minute).
- Store data locally in CSV now, swap to a database later.
- Expose a web API for testing and downstream analysis.

## Project structure
```
src/pricemonitor/
  app/                # Web API wiring (FastAPI stub)
  config/             # Config loader + models
  models/             # Canonical Instrument/Quote models
  providers/          # Provider adapters (Binance, TradingView, IB)
  scheduler/          # Async polling scheduler
  storage/            # Storage backends (CSV now, DB later)
  utils/              # Shared helpers
config/
  sources.yaml        # Providers + instruments
  schedules.yaml      # Per-instrument refresh intervals
  storage.yaml        # Storage backend config
```

## Configuration
- `config/sources.yaml`: providers and instruments
- `config/schedules.yaml`: refresh intervals per symbol/provider
- `config/storage.yaml`: storage backend (CSV)

## Dependencies (when you wire it up)
- `PyYAML` for loading config
- `FastAPI` for the web API
- `Uvicorn` for serving the API

## Run the API (local)
```bash
PYTHONPATH=src uv run uvicorn pricemonitor.app.main:app --reload
```

## Run the polling scheduler (local)
```bash
PYTHONPATH=src uv run pricemonitor-run
```

## Next steps
- Implement TradingView and Interactive Brokers adapters.
- Add backoff/rate-limit handling and retries.
- Add historical queries and analytics.
