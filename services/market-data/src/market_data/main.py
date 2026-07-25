"""Market Data Service entry point."""

import asyncio
from contextlib import AsyncExitStack

import redis.asyncio as redis
from shared_core.config import get_settings
from shared_core.logging import get_logger
from shared_core.messaging import RedisEventBus

from market_data.adapters.binance import BinanceAdapter
from market_data.application.publisher import MarketDataPublisher

logger = get_logger(__name__)


async def main() -> None:
    """Run the market data service."""
    settings = get_settings()
    symbols = ["BTC-USDT", "ETH-USDT"]
    interval = "1m"

    logger.info(
        "market_data_service.starting",
        app_name=settings.app_name,
        redis_url=settings.redis_url,
        symbols=symbols,
        interval=interval,
    )

    redis_client = redis.from_url(settings.redis_url)
    event_bus = RedisEventBus(redis_client)
    publisher = MarketDataPublisher(event_bus)
    adapter = BinanceAdapter()

    async with AsyncExitStack() as stack:
        stack.push_async_callback(redis_client.close)

        async def forward_ticks() -> None:
            async for tick in adapter.stream_ticks(symbols):
                logger.debug("tick.received", symbol=tick.symbol, price=str(tick.price))
                await publisher.publish_tick(tick)

        async def forward_candles() -> None:
            async for candle in adapter.stream_candles(symbols, interval):
                logger.info(
                    "candle.received",
                    symbol=candle.symbol,
                    interval=candle.interval,
                    close=str(candle.close),
                )
                await publisher.publish_candle(candle)

        await asyncio.gather(
            forward_ticks(),
            forward_candles(),
            return_exceptions=True,
        )


if __name__ == "__main__":
    asyncio.run(main())
