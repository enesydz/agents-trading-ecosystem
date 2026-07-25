# API Gateway

External-facing API for the trading ecosystem.

## Responsibility

- Expose REST and WebSocket endpoints for market data, orders, portfolio, and agent interactions.
- Validate all inbound requests.
- Forward requests to the appropriate service or publish commands to the event bus.

## Run Locally

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` — service info
- `GET /health` — liveness
- `GET /health/ready` — readiness
