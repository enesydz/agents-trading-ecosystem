"""Simple moving average indicator."""

from collections import deque
from decimal import Decimal
from typing import ClassVar

from domain_models.market_data import Candle

from strategy.indicators.base import Indicator


class SmaIndicator(Indicator):
    """Simple moving average over the close price."""

    name: ClassVar[str] = "sma"

    def __init__(self, period: int) -> None:
        if period <= 0:
            raise ValueError("period must be positive")
        self._period = period
        self._closes: deque[Decimal] = deque(maxlen=period)

    def update(self, candle: Candle) -> None:
        self._closes.append(candle.close)

    def value(self) -> Decimal | None:
        if len(self._closes) < self._period:
            return None
        return sum(self._closes) / Decimal(self._period)

    def reset(self) -> None:
        self._closes.clear()
