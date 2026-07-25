"""Order Block detection."""

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

from domain_models.market_data import Candle


class OrderBlockType(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"


@dataclass(frozen=True)
class OrderBlock:
    """A detected order block."""

    symbol: str
    exchange: str
    ob_type: OrderBlockType
    top: Decimal
    bottom: Decimal
    timestamp: datetime
    mitigated: bool = False


class OrderBlockDetector:
    """Detects order blocks from a recent candle history."""

    def __init__(self, lookback: int = 5) -> None:
        self._lookback = lookback
        self._history: deque[Candle] = deque(maxlen=lookback * 3)
        self._order_blocks: deque[OrderBlock] = deque(maxlen=50)

    def update(self, candle: Candle) -> list[OrderBlock]:
        """Process a new closed candle and return newly detected OBs."""
        self._history.append(candle)
        self._mitigate(candle)

        if len(self._history) < 3:
            return []

        detected: list[OrderBlock] = []
        recent = list(self._history)
        if len(recent) < 3:
            return detected

        _, curr, next_candle = recent[-3], recent[-2], recent[-1]
        # Detect bullish OB: last down candle before an up swing.
        if (
            curr.close < curr.open
            and next_candle.close > next_candle.open
            and next_candle.close > curr.high
        ):
            ob = OrderBlock(
                symbol=candle.symbol,
                exchange=candle.exchange,
                ob_type=OrderBlockType.BULLISH,
                top=curr.high,
                bottom=curr.low,
                timestamp=curr.timestamp,
            )
            self._order_blocks.append(ob)
            detected.append(ob)
        # Detect bearish OB: last up candle before a down swing.
        elif (
            curr.close > curr.open
            and next_candle.close < next_candle.open
            and next_candle.close < curr.low
        ):
            ob = OrderBlock(
                symbol=candle.symbol,
                exchange=candle.exchange,
                ob_type=OrderBlockType.BEARISH,
                top=curr.high,
                bottom=curr.low,
                timestamp=curr.timestamp,
            )
            self._order_blocks.append(ob)
            detected.append(ob)

        return detected

    def active_blocks(self) -> list[OrderBlock]:
        """Return unmitigated order blocks."""
        return [ob for ob in self._order_blocks if not ob.mitigated]

    def _mitigate(self, candle: Candle) -> None:
        """Mark order blocks as mitigated if price revisits the zone."""
        updated: list[OrderBlock] = []
        for ob in self._order_blocks:
            if ob.mitigated:
                updated.append(ob)
                continue
            if ob.ob_type == OrderBlockType.BULLISH:
                mitigated = candle.low <= ob.top and candle.close >= ob.bottom
            else:
                mitigated = candle.high >= ob.bottom and candle.close <= ob.top
            updated.append(
                OrderBlock(
                    symbol=ob.symbol,
                    exchange=ob.exchange,
                    ob_type=ob.ob_type,
                    top=ob.top,
                    bottom=ob.bottom,
                    timestamp=ob.timestamp,
                    mitigated=mitigated or ob.mitigated,
                )
            )
        self._order_blocks = deque(updated, maxlen=50)
