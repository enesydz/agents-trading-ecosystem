"""Abstract strategy interface."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from domain_models.market_data import Candle, Tick

from strategy.domain.signal import Signal


class Strategy(ABC):
    """Base class for all trading strategies."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique strategy identifier."""

    @abstractmethod
    def on_tick(self, tick: Tick) -> Signal | None:
        """Process a tick and optionally return a signal."""

    @abstractmethod
    def on_candle(self, candle: Candle, history: Sequence[Candle]) -> Signal | None:
        """Process a closed candle and optional history; optionally return a signal."""
