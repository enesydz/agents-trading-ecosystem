"""Tests for the indicator registry."""

from strategy.indicators.base import IndicatorRegistry
from strategy.indicators.rsi import RsiIndicator
from strategy.indicators.sma import SmaIndicator


def test_registry_lists_builtin_indicators() -> None:
    registry = IndicatorRegistry()
    registry.register(SmaIndicator)
    registry.register(RsiIndicator)

    assert registry.list_indicators() == ["rsi", "sma"]


def test_registry_builds_indicator_by_name() -> None:
    registry = IndicatorRegistry()
    registry.register(SmaIndicator)

    indicator = registry.build("sma", period=10)
    assert isinstance(indicator, SmaIndicator)
    assert indicator._period == 10
