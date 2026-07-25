"""Tests for the paper trading execution engine."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from domain_models.events import EventEnvelope, EventMetadata
from domain_models.market_data import Tick
from domain_models.orders import OrderSide
from shared_core.events import EventBus

from execution.application.paper_engine import PaperExecutionEngine


class FakeEventBus(EventBus):
    def __init__(self) -> None:
        self.published: list[tuple[str, EventEnvelope]] = []

    async def publish(self, stream: str, envelope: EventEnvelope) -> None:
        self.published.append((stream, envelope))

    async def subscribe(
        self, stream: str, consumer_group: str, consumer_name: str, handler: object
    ) -> None:
        pass


def _signal_event(symbol: str, direction: str) -> EventEnvelope:
    return EventEnvelope(
        metadata=EventMetadata(
            event_id=str(uuid4()),
            event_type="SignalGenerated",
            source="strategy-engine",
            correlation_id=None,
        ),
        payload={
            "symbol": symbol,
            "exchange": "binance",
            "direction": direction,
            "confidence": "0.5",
            "strategy": "sma_cross_2_4",
        },
    )


def _tick_event(symbol: str, price: Decimal) -> EventEnvelope:
    return EventEnvelope(
        metadata=EventMetadata(
            event_id=str(uuid4()),
            event_type="MarketTick",
            source="market-data",
            correlation_id=None,
        ),
        payload=Tick(
            symbol=symbol,
            exchange="binance",
            timestamp=datetime.now(UTC),
            price=price,
            volume=Decimal(1),
        ).model_dump(mode="json"),
    )


@pytest.mark.asyncio
async def test_signal_without_price_does_not_fill() -> None:
    bus = FakeEventBus()
    engine = PaperExecutionEngine(bus)
    await engine.handle_signal(_signal_event("BTC-USDT", "long"))

    assert len(bus.published) == 0


@pytest.mark.asyncio
async def test_signal_fills_after_tick_price_arrives() -> None:
    bus = FakeEventBus()
    engine = PaperExecutionEngine(bus)

    await engine.handle_signal(_signal_event("BTC-USDT", "long"))
    assert len(bus.published) == 0

    await engine.handle_tick(_tick_event("BTC-USDT", Decimal(50000)))
    assert len(bus.published) == 1
    stream, envelope = bus.published[0]
    assert stream == "execution:fills"
    assert envelope.metadata.event_type == "OrderFilled"
    assert envelope.payload["side"] == OrderSide.BUY.value
    assert envelope.payload["price"] == "50000"
