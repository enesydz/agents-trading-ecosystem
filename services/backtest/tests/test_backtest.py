"""Tests for event-driven backtesting."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from backtest.engine import BacktestEngine
from domain_models.market_data import Candle
from strategy.domain.strategies import SmaCrossStrategy


def test_backtest_closes_a_reversal_and_reports_metrics() -> None:
    start = datetime.now(UTC)
    candles = []
    for index, close in enumerate(["100", "100", "100", "100", "110", "90", "80"]):
        price = Decimal(close)
        candles.append(
            Candle(
                symbol="BTC-USDT", exchange="binance", interval="1m", open=price,
                high=price, low=price, close=price, volume=Decimal(1),
                timestamp=start + timedelta(minutes=index),
            )
        )
    report = BacktestEngine(SmaCrossStrategy(fast_period=2, slow_period=4)).run(candles)
    assert report.trade_count == 2
    assert report.final_equity < report.initial_equity
    assert report.max_drawdown > 0
