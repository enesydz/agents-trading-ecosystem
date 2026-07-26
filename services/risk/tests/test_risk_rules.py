"""Tests for risk sizing and drawdown rules."""

from decimal import Decimal

from strategy.domain.signal import Signal, SignalDirection

from risk.domain.rules import MaxDrawdownRule, PositionSizeRule, RiskContext


def _signal(quantity: str) -> Signal:
    return Signal(
        symbol="BTC-USDT", exchange="binance", direction=SignalDirection.LONG,
        confidence=Decimal("0.5"), quantity=Decimal(quantity), strategy="test",
    )


def test_position_size_rule_uses_signal_quantity() -> None:
    result = PositionSizeRule().check(_signal("2"), RiskContext(max_position_size=Decimal(1)))
    assert not result.passed


def test_max_drawdown_rule_rejects_breached_equity() -> None:
    context = RiskContext(
        peak_equity=Decimal(10000), current_equity=Decimal(8500), max_drawdown=Decimal(1000)
    )
    result = MaxDrawdownRule().check(_signal("0.01"), context)
    assert not result.passed
