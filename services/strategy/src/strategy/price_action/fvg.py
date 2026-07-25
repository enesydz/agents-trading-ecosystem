"""Fair Value Gap detection."""

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

from domain_models.market_data import Candle


class FvgType(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"


@dataclass(frozen=True)
class Fvg:
    """A detected Fair Value Gap."""

    symbol: str
    exchange: str
    fvg_type: FvgType
    top: Decimal
    bottom: Decimal
    timestamp: datetime
    mitigated: bool = False


class FvgDetector:
    """Detects bullish and bearish Fair Value Gaps from recent candles."""

    def __init__(self) -> None:
        self._history: deque[Candle] = deque(maxlen=10)
        self._fvgs: deque[Fvg] = deque(maxlen=50)

    def update(self, candle: Candle) -> list[Fvg]:
        """Process a new closed candle and return newly detected FVGs."""
        self._history.append(candle)
        self._mitigate(candle)

        if len(self._history) < 3:
            return []

        c1, c2, c3 = list(self._history)[-3:]
        detected: list[Fvg] = []

        # Bullish FVG: c1 high < c3 low (gap up)
        if c1.high < c3.low:
            fvg = Fvg(
                symbol=candle.symbol,
                exchange=candle.exchange,
                fvg_type=FvgType.BULLISH,
                top=c3.low,
                bottom=c1.high,
                timestamp=c2.timestamp,
            )
            self._fvgs.append(fvg)
            detected.append(fvg)

        # Bearish FVG: c1 low > c3 high (gap down)
        if c1.low > c3.high:
            fvg = Fvg(
                symbol=candle.symbol,
                exchange=candle.exchange,
                fvg_type=FvgType.BEARISH,
                top=c1.low,
                bottom=c3.high,
                timestamp=c2.timestamp,
            )
            self._fvgs.append(fvg)
            detected.append(fvg)

        return detected

    def active_gaps(self) -> list[Fvg]:
        """Return unmitigated FVGs."""
        return [fvg for fvg in self._fvgs if not fvg.mitigated]

    def _mitigate(self, candle: Candle) -> None:
        """Mark FVGs as mitigated if price revisits the gap."""
        updated: list[Fvg] = []
        for fvg in self._fvgs:
            if fvg.mitigated:
                updated.append(fvg)
                continue
            mitigated = fvg.bottom <= candle.close <= fvg.top
            updated.append(
                Fvg(
                    symbol=fvg.symbol,
                    exchange=fvg.exchange,
                    fvg_type=fvg.fvg_type,
                    top=fvg.top,
                    bottom=fvg.bottom,
                    timestamp=fvg.timestamp,
                    mitigated=mitigated or fvg.mitigated,
                )
            )
        self._fvgs = deque(updated, maxlen=50)
