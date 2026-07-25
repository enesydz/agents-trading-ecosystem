"""End-to-end paper trading flow test."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from domain_models.events import EventEnvelope, EventMetadata
from domain_models.market_data import Candle, Tick
from domain_models.orders import OrderSide
from execution.application.paper_engine import PaperExecutionEngine
from market_data.application.publisher import MarketDataPublisher
from portfolio.application.service import PortfolioService
from shared_core.events import EventBus
from strategy.application.engine import StrategyEngine
from strategy.domain.strategies import SmaCrossStrategy


class InMemoryEventBus(EventBus):
    """Simple in-memory event bus for integration tests."""

    def __init__(self) -> None:
        self.messages: dict[str, list[EventEnvelope]] = {}

    async def publish(self, stream: str, envelope: EventEnvelope) -> None:
        self.messages.setdefault(stream, []).append(envelope)

    async def subscribe(
        self,
        stream: str,
        consumer_group: str,
        consumer_name: str,
        handler: object,
    ) -> None:
        pass

    def drain(self, stream: str) -> list[EventEnvelope]:
        return self.messages.pop(stream, [])


def _envelope(event_type: str, payload: dict) -> EventEnvelope:
    return EventEnvelope(
        metadata=EventMetadata(
            event_id=str(uuid4()),
            event_type=event_type,
            source="test",
            correlation_id=None,
        ),
        payload=payload,
    )


@pytest.mark.asyncio
async def test_signal_to_fill_to_position() -> None:
    """A closed candle produces a signal, which is filled and reflected in the portfolio."""
    bus = InMemoryEventBus()
    portfolio = PortfolioService()
    publisher = MarketDataPublisher(bus)
    engine = StrategyEngine(bus, strategies=[SmaCrossStrategy(fast_period=2, slow_period=4)])
    execution = PaperExecutionEngine(bus)

    # Feed candles that trigger a LONG signal.
    closes = ["100", "100", "100", "100", "100", "110"]
    for close in closes:
        candle = Candle(
            symbol="BTC-USDT",
            exchange="binance",
            interval="1m",
            open=Decimal(100),
            high=Decimal(100),
            low=Decimal(100),
            close=Decimal(close),
            volume=Decimal(1),
            timestamp=datetime.now(UTC),
        )
        await publisher.publish_candle(candle)
        await engine.handle_candle(bus.drain("market:candles")[0])

    # Move signal from strategy output into execution.
    signals = bus.drain("strategy:signals")
    assert len(signals) == 1
    await execution.handle_signal(signals[0])

    # No fill without a price tick.
    fills = bus.drain("execution:fills")
    assert len(fills) == 0

    # Provide a market price so the pending paper order fills.
    tick = Tick(
        symbol="BTC-USDT",
        exchange="binance",
        timestamp=datetime.now(UTC),
        price=Decimal("50000"),
        volume=Decimal(1),
    )
    await publisher.publish_tick(tick)
    await execution.handle_tick(bus.drain("market:ticks")[0])

    fills = bus.drain("execution:fills")
    assert len(fills) == 1
    fill_payload = fills[0].payload
    assert fill_payload["side"] == OrderSide.BUY.value
    assert fill_payload["symbol"] == "BTC-USDT"

    # Apply the fill to the portfolio.
    portfolio.apply_fill(
        symbol=fill_payload["symbol"],
        exchange=fill_payload["exchange"],
        side=OrderSide(fill_payload["side"]),
        quantity=Decimal(fill_payload["quantity"]),
        price=Decimal(fill_payload["price"]),
    )

    position = portfolio.get_position("BTC-USDT", "binance")
    assert position.quantity == Decimal("0.01")
