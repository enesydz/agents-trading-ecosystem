# domain-models

Shared Pydantic domain models used across all services and agents.

## Responsibility

- Define immutable, validated data structures for market data, orders, positions, and events.
- Ensure consistency at every system boundary.

## Models

- `Tick`, `Candle` — market data
- `Order`, `OrderSide`, `OrderType`, `OrderStatus` — order lifecycle
- `EventEnvelope`, `EventMetadata` — event bus wrapper

## Usage

```python
from domain_models import Tick

tick = Tick(symbol="BTC-USD", exchange="example", price="100.00", volume="1.0")
```
