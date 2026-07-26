# Operations

## Local development

Run `scripts/setup.ps1`, start infrastructure with
`docker compose -f infrastructure/docker/docker-compose.yml up -d`, then run
`python -m pytest -q`, `python -m ruff check .`, and `python -m pyright`.

The agent platform uses a deterministic offline provider by default. LLM and
venue clients must be injected; no credential is required for tests.

## Trading safety

Paper execution is the default. `LiveExchangeAdapter` starts with its kill
switch active and requires the exact confirmation string
`ENABLE_LIVE_TRADING`. The production deployment must keep
`LIVE_TRADING_ENABLED=false` until a reviewed change enables it. Prometheus
alerts cover kill-switch and execution circuit-breaker states.

## Recovery

Run `scripts/backup.ps1` after the PostgreSQL container is healthy. Store the
generated SQL outside the host and test restoration regularly. Kubernetes
manifests are intentionally minimal and require an operator-provided secret,
image registry, ingress, TLS, storage class, and network egress policy.

## Load testing

With the API running, use `python tools/load_test.py --requests 100` for a
latency smoke test. It is not a capacity certification; production limits must
be established from representative traffic and venue rate limits.
