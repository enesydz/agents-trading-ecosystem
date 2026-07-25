"""Liquidity pool detection."""

from collections import deque
from dataclasses import dataclass
from decimal import Decimal

from domain_models.market_data import Candle


@dataclass(frozen=True)
class LiquidityPool:
    """A liquidity zone formed by equal highs or equal lows."""

    symbol: str
    exchange: str
    level: Decimal
    is_high: bool
    touches: int


class LiquidityDetector:
    """Detects equal highs and equal lows as liquidity pools."""

    def __init__(self, lookback: int = 10, tolerance: Decimal = Decimal("0.001")) -> None:
        self._lookback = lookback
        self._tolerance = tolerance
        self._history: deque[Candle] = deque(maxlen=lookback)

    def update(self, candle: Candle) -> list[LiquidityPool]:
        """Process a new closed candle and return detected liquidity pools."""
        self._history.append(candle)
        if len(self._history) < 3:
            return []

        recent = list(self._history)
        pools: list[LiquidityPool] = []
        pools.extend(self._find_equal_levels(recent, is_high=True))
        pools.extend(self._find_equal_levels(recent, is_high=False))
        return pools

    def _find_equal_levels(self, candles: list[Candle], is_high: bool) -> list[LiquidityPool]:
        values = [c.high for c in candles] if is_high else [c.low for c in candles]
        if len(values) < 3:
            return []

        # Check the last value against previous values within tolerance.
        last = values[-1]
        matches = [v for v in values[:-1] if abs(v - last) <= self._tolerance * last]
        if not matches:
            return []

        return [
            LiquidityPool(
                symbol=candles[-1].symbol,
                exchange=candles[-1].exchange,
                level=last,
                is_high=is_high,
                touches=len(matches) + 1,
            )
        ]
