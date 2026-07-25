"""Tests for liquidity pool detection."""

from datetime import UTC, datetime
from decimal import Decimal

from domain_models.market_data import Candle

from strategy.price_action.liquidity import LiquidityDetector


def _candle(price: str) -> Candle:
    p = Decimal(price)
    return Candle(
        symbol="BTC-USDT",
        exchange="binance",
        interval="1m",
        open=p,
        high=p + Decimal("0.1"),
        low=p - Decimal("0.1"),
        close=p,
        volume=Decimal(1),
        timestamp=datetime.now(UTC),
    )


def test_equal_high_liquidity_detected() -> None:
    detector = LiquidityDetector(lookback=5, tolerance=Decimal("0.01"))
    candles = [
        _candle("100"),
        _candle("101"),
        _candle("100"),
        _candle("100"),
    ]
    for candle in candles:
        detector.update(candle)

    # Equal highs around 100.1 (high of the _candle helper)
    pools = detector.update(_candle("100"))
    assert any(pool.is_high and pool.level == Decimal("100.1") for pool in pools)
