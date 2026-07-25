# Roadmap

## Legend

- `P0`: Foundation. Required before any trading feature.
- `P1`: Core trading capability.
- `P2`: Advanced features and AI integration.
- `P3`: Scale, optimization, and enterprise features.

## Phase 0 — Foundation (Weeks 1–2)

- [x] Define architecture and project structure
- [x] Containerized local development environment (Docker Compose)
- [x] Shared core package: logging, config, events, messaging abstractions
- [x] Domain models package: Pydantic models for market data, orders, positions
- [x] CI skeleton: lint, type check, unit tests
- [x] Developer documentation and coding standards

## Phase 1 — Market Data & Core Services (Weeks 3–5)

- [x] Market Data Service: WebSocket ingestion for one exchange (Binance)
- [x] Normalized tick/candle event schema
- [x] Redis Streams event bus
- [x] Portfolio Service: position and balance tracking
- [x] Execution Service: paper trading adapter
- [x] Order lifecycle state machine
- [x] API Gateway: health, market data, and portfolio endpoints
- [x] End-to-end paper trading test

## Phase 2 — Strategy & Risk (Weeks 6–9)

- [ ] Indicator engine plugin architecture
- [ ] Strategy engine with event-driven signal generation
- [ ] Basic TA strategies (SMA crossover, RSI)
- [ ] Price-action structures: Order Blocks, FVG, liquidity
- [ ] Risk engine: position sizing, max drawdown, daily loss limit
- [ ] Backtest engine: event-driven simulation
- [ ] Strategy performance analytics

## Phase 3 — AI Agents (Weeks 10–14)

- [ ] Agent orchestrator and memory layer
- [ ] Trading Assistant: structured event reasoning + NL response
- [ ] Market Analyst agent: narrative generation and market structure summary
- [ ] RAG over market events and documentation
- [ ] Tool calling: query market state, place paper orders, run backtests
- [ ] Evaluation pipeline for agent outputs

## Phase 4 — Production Readiness (Weeks 15–18)

- [ ] Live exchange adapter with kill switch
- [ ] Advanced monitoring, alerting, and circuit breakers
- [ ] Disaster recovery and backup procedures
- [ ] Security audit and secrets rotation
- [ ] Load testing and latency profiling
- [ ] Kubernetes manifests and Terraform modules

## Phase 5 — Scale & Autonomy (Ongoing)

- [ ] Multi-exchange arbitrage and smart order routing
- [ ] Online strategy optimization and meta-learning
- [ ] Continuous self-improvement loop
- [ ] Multi-asset class support
- [ ] Regulated market connectivity

## Current Focus

Complete Phase 0 and begin Phase 1. The immediate next step after this document is to implement the Docker Compose local environment and the `shared-core` package.
