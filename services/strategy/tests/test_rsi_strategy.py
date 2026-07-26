"""Tests for the RSI strategy."""

from datetime import UTC, datetime
from decimal import Decimal

from domain_models.market_data import Candle

from strategy.domain.signal import SignalDirection
from strategy.domain.strategies import RsiStrategy


def test_rsi_strategy_signals_long_when_oversold() -> None:
    strategy = RsiStrategy(period=3, oversold=Decimal(40), overbought=Decimal(60))
    signal = None
    for close in ["100", "99", "98", "97"]:
        value = Decimal(close)
        signal = strategy.on_candle(
            Candle(
                symbol="BTC-USDT", exchange="binance", interval="1m", open=value,
                high=value, low=value, close=value, volume=Decimal(1),
                timestamp=datetime.now(UTC),
            ),
            history=(),
        )
    assert signal is not None
    assert signal.direction == SignalDirection.LONG
