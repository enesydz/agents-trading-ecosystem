"""Strategy engine that consumes market events and emits signals."""

from collections import defaultdict, deque
from uuid import uuid4

from domain_models.events import EventEnvelope
from domain_models.market_data import Candle, Tick
from shared_core.events import EventBus

from strategy.domain.signal import Signal
from strategy.domain.strategy import Strategy


class StrategyEngine:
    """Routes market data to registered strategies and publishes signals."""

    SIGNAL_STREAM = "strategy:signals"

    def __init__(self, event_bus: EventBus, strategies: list[Strategy]) -> None:
        self._bus = event_bus
        self._strategies = strategies
        self._history: dict[str, deque[Candle]] = defaultdict(lambda: deque(maxlen=500))

    async def handle_tick(self, envelope: EventEnvelope) -> None:
        """Handle a MarketTick event."""
        tick = Tick.model_validate(envelope.payload)
        for strategy in self._strategies:
            signal = strategy.on_tick(tick)
            if signal is not None:
                await self._publish_signal(signal)

    async def handle_candle(self, envelope: EventEnvelope) -> None:
        """Handle a MarketCandle event."""
        candle = Candle.model_validate(envelope.payload)
        history = self._history[candle.symbol]
        for strategy in self._strategies:
            signal = strategy.on_candle(candle, history=tuple(history))
            if signal is not None:
                await self._publish_signal(signal)
        history.append(candle)

    async def _publish_signal(self, signal: Signal) -> None:
        envelope = EventEnvelope.create(
            event_type="SignalGenerated",
            source="strategy-engine",
            payload=signal.model_dump(mode="json"),
            event_id=str(uuid4()),
        )
        await self._bus.publish(self.SIGNAL_STREAM, envelope)
