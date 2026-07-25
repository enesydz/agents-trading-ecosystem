# shared-core

Shared infrastructure utilities for the trading ecosystem.

## Responsibility

- Configuration management via Pydantic Settings.
- Structured logging with structlog.
- Event bus abstraction and Redis Streams implementation.
- Common helpers that do not belong to a specific domain.

## Usage

```python
from shared_core import get_logger, get_settings

logger = get_logger(__name__)
settings = get_settings()
```
