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

- [x] Indicator engine plugin architecture
- [x] Strategy engine with event-driven signal generation
- [x] Basic TA strategies (SMA crossover, RSI)
- [x] Price-action structures: Order Blocks, FVG, liquidity
- [x] Risk engine: position sizing, max drawdown, daily loss limit
- [x] Backtest engine: event-driven simulation
- [x] Strategy performance analytics

## Phase 3 — AI Agents (Weeks 10–14)

- [x] Agent orchestrator and memory layer
- [x] Trading Assistant: structured event reasoning + NL response
- [x] Market Analyst agent: narrative generation and market structure summary
- [x] RAG over market events and documentation
- [x] Tool calling: query market state, place paper orders, run backtests
- [x] Evaluation pipeline for agent outputs

## Phase 4 — Production Readiness (Weeks 15–18)

- [x] Live exchange adapter with kill switch
- [x] Advanced monitoring, alerting, and circuit breakers
- [x] Disaster recovery and backup procedures
- [x] Security audit and secrets rotation
- [x] Load testing and latency profiling
- [x] Kubernetes manifests and Terraform modules

## Phase 5 — Scale & Autonomy (Ongoing)

- [x] Multi-exchange arbitrage and smart order routing
- [x] Online strategy optimization and meta-learning
- [x] Continuous self-improvement loop
- [x] Multi-asset class support
- [x] Regulated market connectivity

## Current Focus

All roadmap phases are implemented as a safe, provider-agnostic reference platform. Live venue credentials and infrastructure-specific deployment values remain explicit operator configuration.
