# ADR-001: Initial Architecture for AI Trading Ecosystem

## Status

Accepted

## Context

We are building an autonomous AI-powered trading ecosystem from scratch. The system must support real-time market data, strategy execution, risk management, portfolio tracking, backtesting, paper/live trading, and AI agents. The architecture must scale for years without major redesign.

## Decision

Adopt a **modular, event-driven, monorepo architecture** with Docker Compose for local development and a clear migration path to microservices and Kubernetes.

Key choices:

1. **Monorepo**: Use a single repository with `/apps`, `/services`, `/packages`, `/agents`, `/infrastructure`, and `/docs`.
2. **Event-Driven Communication**: Services publish and subscribe to normalized events via Redis Streams initially, with Kafka as a future option.
3. **Clean Architecture / DDD**: Business logic isolated from frameworks and infrastructure; folder structure reflects bounded contexts.
4. **Python First**: Primary language is Python 3.12+ for quant, ML, and AI ecosystems.
5. **FastAPI for API Gateway**: Async-native, OpenAPI generation, high performance.
6. **PostgreSQL + pgvector**: Single store for relational data and vector memory.
7. **Redis**: Cache, pub/sub, and lightweight event streams.
8. **Plugin Architecture**: Strategies, indicators, risk rules, and exchange adapters are plugins.
9. **Observability First**: Prometheus, Grafana, Loki, and Tempo from day one.
10. **AI Agents as First-Class Services**: Agents consume structured market events and maintain memory via RAG.

## Consequences

### Positive

- Clear domain boundaries reduce coupling and enable independent scaling later.
- Event-driven design supports replay, backtesting, and auditability.
- Plugin architecture allows rapid experimentation without core changes.
- Single database for relational + vector data reduces operational complexity early.
- Strong observability foundations prevent debugging in production later.

### Negative

- Redis Streams has lower throughput than Kafka; may need migration at high scale.
- Monorepo requires disciplined package boundaries to avoid tight coupling.
- Python's concurrency model may require careful async design for high-frequency data.

## Alternatives Considered

- **Microservices from day one**: Rejected. Adds unnecessary operational complexity before product-market fit.
- **Direct RPC between services**: Rejected. Couples services tightly and complicates replay/backtesting.
- **Separate vector database**: Rejected. Adds operational overhead; pgvector is sufficient for early scale.

## Related Decisions

- ADR-002: Event Schema and Versioning (to be written)
- ADR-003: Plugin Architecture for Strategies (to be written)
- ADR-004: Agent Memory and RAG Design (to be written)

## Date

2026-07-26
