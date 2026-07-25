"""Tests for the SMA crossover strategy."""

from datetime import UTC, datetime
from decimal import Decimal

from domain_models.market_data import Candle

from strategy.domain.signal import SignalDirection
from strategy.domain.strategies import SmaCrossStrategy


def _candle(close: str) -> Candle:
    return Candle(
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


def test_sma_cross_generates_long_signal() -> None:
    strategy = SmaCrossStrategy(fast_period=2, slow_period=4)
    # Prices start equal to the average then accelerate above the slow average to trigger LONG.
    closes = ["100", "100", "100", "100", "100", "110"]
    signal = None
    for close in closes:
        signal = strategy.on_candle(_candle(close), history=[])

    assert signal is not None
    assert signal.direction == SignalDirection.LONG
    assert signal.symbol == "BTC-USDT"
    assert signal.strategy == "sma_cross_2_4"


def test_sma_cross_no_signal_with_insufficient_data() -> None:
    strategy = SmaCrossStrategy(fast_period=5, slow_period=20)
    signal = strategy.on_candle(_candle("100"), history=[])
    assert signal is None
