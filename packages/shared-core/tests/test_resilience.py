"""Tests for shared resilience primitives."""

from shared_core.resilience import CircuitBreaker, CircuitState


def test_circuit_breaker_fails_closed() -> None:
    breaker = CircuitBreaker(failure_threshold=2, recovery_seconds=60)
    breaker.failure()
    assert breaker.allow()
    breaker.failure()
    assert breaker.state == CircuitState.OPEN
    assert not breaker.allow()
