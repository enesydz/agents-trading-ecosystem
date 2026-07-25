# Coding Standards

## General Principles

- Single Responsibility: every file, class, and function does one thing well.
- Small modules: prefer many small modules over a few large ones.
- High cohesion, low coupling.
- Strong typing: use type hints everywhere.
- Self-documenting code: clear names over comments.
- No duplicated logic.
- No dead code.
- No demo code or quick hacks.

## Python

- Use Python 3.12+ features where appropriate.
- Format with **Ruff**.
- Type-check with **pyright** or **mypy** in strict mode.
- Use **Pydantic v2** for all data models and validation.
- Use **pytest** for tests; aim for high coverage on domain logic.
- Use `async`/`await` for I/O-bound code.
- Avoid mixing sync and async code.
- Log with structlog; never log secrets.

## Naming

| Construct | Convention | Example |
|---|---|---|
| Module | snake_case | `market_data_service.py` |
| Class | PascalCase | `MarketDataService` |
| Function / method | snake_case | `publish_tick_event` |
| Constant | SCREAMING_SNAKE_CASE | `MAX_POSITION_SIZE` |
| Variable | snake_case | `current_price` |
| Environment variable | SCREAMING_SNAKE_CASE | `REDIS_URL` |
| Private member | leading underscore | `_internal_state` |

## Project Layout

Each service or package follows this internal structure:

```text
my_service/
  pyproject.toml
  src/
    my_service/
      __init__.py
      domain/        # Pure business logic, no framework deps
      application/   # Use cases, service orchestration
      infrastructure/# Adapters: db, messaging, exchange clients
      interfaces/    # API controllers, CLI, event handlers
      config.py      # Settings via Pydantic Settings
      main.py        # Entry point
  tests/
    unit/
    integration/
```

## Dependencies

- Prefer explicit dependencies in `pyproject.toml`.
- Pin versions for reproducibility.
- Separate `dev`, `test`, and `prod` dependency groups.
- Audit new dependencies before adding them.

## Testing

- Unit tests: fast, isolated, deterministic.
- Integration tests: verify service boundaries with test containers.
- E2E tests: verify critical user journeys.
- Property-based tests for calculation-heavy modules.

## Documentation

- Update `Architecture.md` when architectural assumptions change.
- Create an ADR for every significant decision.
- Keep `Roadmap.md` current.
- Document public APIs with OpenAPI annotations.

## Security

- Secrets in environment variables or a vault; never in code.
- Validate all inputs at boundaries.
- Use parameterized queries; avoid raw SQL concatenation.
- Encrypt exchange keys at rest.
