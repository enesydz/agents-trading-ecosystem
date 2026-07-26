"""Reusable circuit breaker for external dependencies."""

from enum import Enum
from time import monotonic


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Fail closed after repeated errors and recover after a cool-down."""

    def __init__(self, failure_threshold: int = 3, recovery_seconds: float = 30) -> None:
        if failure_threshold <= 0 or recovery_seconds <= 0:
            raise ValueError("circuit breaker limits must be positive")
        self.failure_threshold = failure_threshold
        self.recovery_seconds = recovery_seconds
        self.failures = 0
        self.opened_at: float | None = None
        self.state = CircuitState.CLOSED

    def allow(self) -> bool:
        if self.state == CircuitState.OPEN and self.opened_at is not None:
            if monotonic() - self.opened_at >= self.recovery_seconds:
                self.state = CircuitState.HALF_OPEN
            else:
                return False
        return True

    def success(self) -> None:
        self.failures = 0
        self.opened_at = None
        self.state = CircuitState.CLOSED

    def failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = monotonic()
