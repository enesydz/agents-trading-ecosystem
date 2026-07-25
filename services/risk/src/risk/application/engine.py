"""Risk engine application service."""

from uuid import uuid4

from domain_models.events import EventEnvelope
from shared_core.events import EventBus
from shared_core.logging import get_logger
from strategy.domain.signal import Signal

from risk.domain.rules import DailyLossLimitRule, KillSwitchRule, PositionSizeRule, RiskContext

logger = get_logger(__name__)


class RiskEngine:
    """Evaluates trading signals against risk rules."""

    VALIDATED_STREAM = "risk:validated"
    REJECTED_STREAM = "risk:rejected"

    def __init__(self, event_bus: EventBus) -> None:
        self._bus = event_bus
        self._rules = [KillSwitchRule(), DailyLossLimitRule(), PositionSizeRule()]
        self._context = RiskContext()

    def update_context(self, **kwargs: object) -> None:
        """Update the risk context fields."""
        for key, value in kwargs.items():
            setattr(self._context, key, value)

    async def handle_signal(self, envelope: EventEnvelope) -> None:
        """Validate a SignalGenerated event and emit result."""
        signal = Signal.model_validate(envelope.payload)
        results = [rule.check(signal, self._context) for rule in self._rules]
        failed = [r for r in results if not r.passed]

        if failed:
            reason = "; ".join(f"{r.rule}: {r.message}" for r in failed)
            logger.warning("risk.signal_rejected", signal=str(signal.symbol), reason=reason)
            await self._publish("SignalRejected", signal, reason)
        else:
            logger.info("risk.signal_validated", signal=str(signal.symbol))
            await self._publish("RiskValidated", signal, "")

    async def _publish(self, event_type: str, signal: Signal, reason: str) -> None:
        stream = self.REJECTED_STREAM if event_type == "SignalRejected" else self.VALIDATED_STREAM
        envelope = EventEnvelope.create(
            event_type=event_type,
            source="risk-engine",
            payload={
                "signal": signal.model_dump(mode="json"),
                "reason": reason,
            },
            event_id=str(uuid4()),
        )
        await self._bus.publish(stream, envelope)
