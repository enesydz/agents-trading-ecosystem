# Strategy Engine

Generates trading signals from market data events.

## Responsibility

- Subscribe to market ticks and candles.
- Run registered strategies.
- Publish `SignalGenerated` events to the event bus.

## Strategies

- `SmaCrossStrategy` — Simple moving average crossover.

## Run Locally

```bash
python -m strategy.infrastructure.subscriber
```
