"""Redis Streams consumer for market data events."""

import asyncio

import redis.asyncio as redis
from shared_core.config import get_settings
from shared_core.logging import get_logger
from shared_core.messaging import RedisEventBus

from strategy.application.engine import StrategyEngine
from strategy.domain.strategies import SmaCrossStrategy

logger = get_logger(__name__)


async def run_strategy_engine() -> None:
    """Start the strategy engine and consume market events."""
    settings = get_settings()
    redis_client = redis.from_url(settings.redis_url)
    event_bus = RedisEventBus(redis_client)
    engine = StrategyEngine(event_bus, strategies=[SmaCrossStrategy()])

    async with asyncio.TaskGroup() as group:
        group.create_task(
            event_bus.subscribe(
                stream="market:ticks",
                consumer_group="strategy-engine",
                consumer_name="strategy-engine-1",
                handler=engine.handle_tick,
            )
        )
        group.create_task(
            event_bus.subscribe(
                stream="market:candles",
                consumer_group="strategy-engine",
                consumer_name="strategy-engine-1",
                handler=engine.handle_candle,
            )
        )


if __name__ == "__main__":
    asyncio.run(run_strategy_engine())
