"""Market data event publisher."""

from uuid import uuid4

from domain_models.events import EventEnvelope
from domain_models.market_data import Candle, Tick
from shared_core.events import EventBus


class MarketDataPublisher:
    """Publishes normalized market data events to the event bus."""

    TICK_STREAM = "market:ticks"
    CANDLE_STREAM = "market:candles"

    def __init__(self, event_bus: EventBus, source: str = "market-data") -> None:
        self._bus = event_bus
        self._source = source

    async def publish_tick(self, tick: Tick) -> None:
        """Publish a single tick event."""
        envelope = EventEnvelope.create(
            event_type="MarketTick",
            source=self._source,
            payload=tick.model_dump(mode="json"),
            event_id=str(uuid4()),
        )
        await self._bus.publish(self.TICK_STREAM, envelope)

    async def publish_candle(self, candle: Candle) -> None:
        """Publish a single closed-candle event."""
        envelope = EventEnvelope.create(
            event_type="MarketCandle",
            source=self._source,
            payload=candle.model_dump(mode="json"),
            event_id=str(uuid4()),
        )
        await self._bus.publish(self.CANDLE_STREAM, envelope)
