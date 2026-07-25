"""Tests for order block detection."""

from datetime import UTC, datetime
from decimal import Decimal

from domain_models.market_data import Candle

from strategy.price_action.order_blocks import (
    OrderBlockDetector,
    OrderBlockType,
)


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


def test_bullish_order_block_detected() -> None:
    detector = OrderBlockDetector(lookback=5)
    # Down move then strong bullish reversal.
    candles = [
        _candle("100", "100", "99", "99"),
        _candle("99", "96", "95", "95"),  # bearish curr with small high
        _candle("95", "97", "95", "97"),  # bullish next closes above curr.high
        _candle("97", "102", "97", "102"),  # low=97 stays above OB top=96
    ]
    for candle in candles:
        detector.update(candle)

    active = detector.active_blocks()
    assert len(active) == 1
    assert active[0].ob_type == OrderBlockType.BULLISH
