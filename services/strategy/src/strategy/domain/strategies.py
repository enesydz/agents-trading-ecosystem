"""Built-in example strategies."""

from collections.abc import Sequence
from decimal import Decimal

from domain_models.market_data import Candle, Tick

from strategy.domain.signal import Signal, SignalDirection
from strategy.domain.strategy import Strategy
from strategy.indicators.base import Indicator, IndicatorRegistry
from strategy.indicators.rsi import RsiIndicator
from strategy.indicators.sma import SmaIndicator

# Register built-in indicators at module import time.
_default_registry = IndicatorRegistry()
_default_registry.register(SmaIndicator)
_default_registry.register(RsiIndicator)


class SmaCrossStrategy(Strategy):
    """Simple moving average crossover strategy using the indicator engine."""

    def __init__(
        self,
        fast_period: int = 5,
        slow_period: int = 20,
        registry: IndicatorRegistry | None = None,
    ) -> None:
        self._fast_period = fast_period
        self._slow_period = slow_period
        self._registry = registry or _default_registry
        self._fast_indicators: dict[str, Indicator] = {}
        self._slow_indicators: dict[str, Indicator] = {}
        self._last_direction: dict[str, SignalDirection | None] = {}

    @property
    def name(self) -> str:
        return f"sma_cross_{self._fast_period}_{self._slow_period}"

    def on_tick(self, tick: Tick) -> Signal | None:
        return None

    def on_candle(self, candle: Candle, history: Sequence[Candle]) -> Signal | None:
        fast = self._get_indicator(candle.symbol, "fast", self._fast_period, self._fast_indicators)
        slow = self._get_indicator(candle.symbol, "slow", self._slow_period, self._slow_indicators)

        fast.update(candle)
        slow.update(candle)

        fast_sma = fast.value()
        slow_sma = slow.value()
        if fast_sma is None or slow_sma is None:
            return None

        direction: SignalDirection | None = None
        if fast_sma > slow_sma:
            direction = SignalDirection.LONG
        elif fast_sma < slow_sma:
            direction = SignalDirection.SHORT

        last = self._last_direction.get(candle.symbol)
        if direction is None or direction == last:
            return None

        self._last_direction[candle.symbol] = direction
        return Signal(
            symbol=candle.symbol,
            exchange=candle.exchange,
            direction=direction,
            confidence=Decimal("0.5"),
            strategy=self.name,
            metadata={
                "fast_sma": float(fast_sma),
                "slow_sma": float(slow_sma),
            },
        )

    def _get_indicator(
        self,
        symbol: str,
        label: str,
        period: int,
        cache: dict[str, Indicator],
    ) -> Indicator:
        key = f"{symbol}:{label}"
        if key not in cache:
            indicator = self._registry.build("sma", period=period)
            cache[key] = indicator
        return cache[key]
