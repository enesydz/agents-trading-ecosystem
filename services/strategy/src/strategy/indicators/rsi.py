"""Relative strength index indicator."""

from collections import deque
from decimal import Decimal
from typing import ClassVar

from domain_models.market_data import Candle

from strategy.indicators.base import Indicator


class RsiIndicator(Indicator):
    """Relative Strength Index (RSI) over the close price."""

    name: ClassVar[str] = "rsi"

    def __init__(self, period: int = 14) -> None:
        if period <= 0:
            raise ValueError("period must be positive")
        self._period = period
        self._closes: deque[Decimal] = deque(maxlen=period + 1)

    def update(self, candle: Candle) -> None:
        self._closes.append(candle.close)

    def value(self) -> Decimal | None:
        if len(self._closes) < self._period + 1:
            return None
        gains = Decimal(0)
        losses = Decimal(0)
        closes = list(self._closes)
        for i in range(1, self._period + 1):
            change = closes[i] - closes[i - 1]
            if change > 0:
                gains += change
            else:
                losses -= change
        avg_gain = gains / Decimal(self._period)
        avg_loss = losses / Decimal(self._period)
        if avg_loss == 0:
            return Decimal(100)
        rs = avg_gain / avg_loss
        return Decimal(100) - (Decimal(100) / (Decimal(1) + rs))

    def reset(self) -> None:
        self._closes.clear()
