# Risk Engine

Validates trading signals and orders against risk rules.

## Responsibility

- Evaluate signals against position limits, exposure, and drawdown rules.
- Emit `RiskValidated` or `RiskRejected` events.
- Provide kill-switch and global risk status.
