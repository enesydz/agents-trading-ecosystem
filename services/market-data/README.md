# Market Data Service

Ingests, normalizes, and publishes market data from exchanges.

## Responsibility

- Maintain WebSocket and REST connections to exchanges.
- Normalize ticks and candles into the shared domain model.
- Publish events to Redis Streams for downstream consumers.
- Provide historical data queries.

## Run Locally

```bash
python -m market_data.main
```
