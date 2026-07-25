# Portfolio Service

Tracks positions, balances, and PnL across accounts.

## Responsibility

- Maintain positions per symbol and exchange.
- Update PnL on market price changes and fills.
- Provide portfolio snapshots via query interface.
- Consume `OrderFilled` events.
