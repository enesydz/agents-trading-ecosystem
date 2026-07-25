"""Tests for the SMA indicator."""

from datetime import UTC, datetime
from decimal import Decimal

from domain_models.market_data import Candle

from strategy.indicators.sma import SmaIndicator


def _candle(close: Decimal) -> Candle:
    return Candle(
        symbol="BTC-USDT",
        exchange="binance",
        interval="1m",
        open=close,
        high=close,
        low=close,
        close=close,
        volume=Decimal(1),
        timestamp=datetime.now(UTC),
    )


def test_sma_not_ready_until_period_full() -> None:
    sma = SmaIndicator(period=3)
    assert sma.value() is None
    sma.update(_candle(Decimal(10)))
    sma.update(_candle(Decimal(20)))
    assert sma.value() is None
    sma.update(_candle(Decimal(30)))
    assert sma.value() == Decimal(20)


def test_sma_sliding_window() -> None:
    sma = SmaIndicator(period=3)
    for value in [Decimal(10), Decimal(20), Decimal(30), Decimal(60)]:
        sma.update(_candle(value))
    assert sma.value() == Decimal(30 + 60 + 20) / Decimal(3)
