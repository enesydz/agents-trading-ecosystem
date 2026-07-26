"""Live execution boundary with mandatory kill switch and circuit breaker."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain_models.orders import Order


@dataclass(frozen=True)
class LiveExecutionResult:
    """Normalized result from a live venue."""

    accepted: bool
    venue_order_id: str | None
    reason: str = ""


class LiveExchangeAdapter(ABC):
    """Base adapter; implementations must explicitly enforce safety state."""

    def __init__(self) -> None:
        self.kill_switch = True
        self.failure_count = 0
        self.failure_limit = 3

    def enable(self, confirmation: str) -> None:
        if confirmation != "ENABLE_LIVE_TRADING":
            raise ValueError("explicit live trading confirmation required")
        self.kill_switch = False

    def disable(self) -> None:
        self.kill_switch = True

    async def submit(self, order: Order) -> LiveExecutionResult:
        if self.kill_switch:
            return LiveExecutionResult(False, None, "kill switch is active")
        if self.failure_count >= self.failure_limit:
            return LiveExecutionResult(False, None, "circuit breaker is open")
        try:
            return await self._submit(order)
        except RuntimeError as exc:
            self.failure_count += 1
            return LiveExecutionResult(False, None, f"venue error: {exc}")

    @abstractmethod
    async def _submit(self, order: Order) -> LiveExecutionResult:
        """Submit an order using a concrete authenticated venue client."""


class DryRunLiveAdapter(LiveExchangeAdapter):
    """Contract-test adapter that never contacts an exchange."""

    async def _submit(self, order: Order) -> LiveExecutionResult:
        return LiveExecutionResult(True, f"dry-run-{order.id}", "dry run")
