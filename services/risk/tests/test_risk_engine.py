"""Tests for the risk engine."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from domain_models.events import EventEnvelope, EventMetadata
from shared_core.events import EventBus
from strategy.domain.signal import Signal, SignalDirection

from risk.application.engine import RiskEngine


class FakeEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[tuple[str, EventEnvelope]] = []

    async def publish(self, stream: str, envelope: EventEnvelope) -> None:
        self.published.append((stream, envelope))

    async def subscribe(
        self,
        stream: str,
        consumer_group: str,
        consumer_name: str,
        handler: object,
    ) -> None:
        pass


def _signal_event() -> EventEnvelope:
    signal = Signal(
        symbol="BTC-USDT",
        exchange="binance",
        direction=SignalDirection.LONG,
        confidence=Decimal("0.5"),
        strategy="sma_cross",
        timestamp=datetime.now(UTC),
    )
    return EventEnvelope(
        metadata=EventMetadata(
            event_id=str(uuid4()),
            event_type="SignalGenerated",
            source="strategy-engine",
            correlation_id=None,
        ),
        payload=signal.model_dump(mode="json"),
    )


@pytest.mark.asyncio
async def test_signal_passes_default_risk_rules() -> None:
    bus = FakeEventBus()
    engine = RiskEngine(bus)
    await engine.handle_signal(_signal_event())

    assert len(bus.published) == 1
    stream, envelope = bus.published[0]
    assert stream == "risk:validated"
    assert envelope.metadata.event_type == "RiskValidated"


@pytest.mark.asyncio
async def test_signal_rejected_when_kill_switch_active() -> None:
    bus = FakeEventBus()
    engine = RiskEngine(bus)
    engine.update_context(kill_switch_active=True)
    await engine.handle_signal(_signal_event())

    assert len(bus.published) == 1
    stream, envelope = bus.published[0]
    assert stream == "risk:rejected"
    assert envelope.metadata.event_type == "SignalRejected"
