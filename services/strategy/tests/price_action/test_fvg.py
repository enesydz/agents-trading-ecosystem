"""Tests for Fair Value Gap detection."""

from datetime import UTC, datetime
from decimal import Decimal

from domain_models.market_data import Candle

from strategy.price_action.fvg import FvgDetector, FvgType


def _candle(open_p: str, high: str, low: str, close: str) -> Candle:
    return Candle(
        symbol="BTC-USDT",
        exchange="binance",
        interval="1m",
        open=Decimal(open_p),
        high=Decimal(high),
        low=Decimal(low),
        close=Decimal(close),
        volume=Decimal(1),
        timestamp=datetime.now(UTC),
    )


def test_bullish_fvg_detected() -> None:
    detector = FvgDetector()
    candles = [
        _candle("100", "101", "100", "100"),
        _candle("102", "103", "102", "102"),
        _candle("104", "105", "104", "104"),
    ]
    for candle in candles:
        detector.update(candle)

    active = detector.active_gaps()
    assert len(active) == 1
    assert active[0].fvg_type == FvgType.BULLISH
    assert active[0].bottom == Decimal(101)
    assert active[0].top == Decimal(104)
