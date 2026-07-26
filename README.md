# Agents — Autonomous AI Trading Ecosystem

An enterprise-grade, event-driven trading platform built for autonomous AI agents, quantitative strategies, and long-term growth.

## Status

Reference platform complete. Core trading, strategy/risk, AI agents, production safety,
deployment manifests, routing, and optimization primitives are implemented. Live trading
remains disabled until an operator supplies venue-specific credentials and explicit approval.

## Quick Start

### Prerequisites

- Docker + Docker Compose
- Python 3.12+
- Node.js 20+ (for web frontend later)
- Git

### Run Local Environment

```bash
# Clone and enter the repository
cd c:\Users\Admin\Desktop\projects\Agents

# Start infrastructure services (Redis, PostgreSQL, monitoring)
docker compose -f infrastructure/docker/docker-compose.yml up -d

# Install all packages (run from repository root)
scripts/setup.ps1

# Run tests
python -m pytest -q
```

## Project Structure

```text
/apps          # User-facing applications (API gateway, web UI)
/services      # Domain services (market data, execution, strategy, risk, etc.)
/agents        # AI agents (trading assistant, market analyst)
/packages      # Shared libraries (domain models, shared core)
/infrastructure # Docker, Terraform, Kubernetes manifests
/docs          # Architecture, roadmap, ADRs, guides
/tests         # Cross-service tests
/config        # Configuration templates
/scripts       # Developer automation
/monitoring    # Observability configuration
/tools         # Utility scripts
```

## Documentation

- [Architecture](docs/Architecture.md)
- [Roadmap](docs/Roadmap.md)
- [Operations and deployment](docs/Operations.md)
- [Coding Standards](docs/guides/Coding-Standards.md)
- [Decisions](docs/decisions/)

## Contributing

1. Follow the architecture and coding standards.
2. Write tests for domain logic.
3. Update documentation and ADRs when making significant changes.
4. Never commit secrets.

## License

Proprietary — see LICENSE (to be added).
