"""Abstract exchange adapter interface."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from domain_models.market_data import Candle, Tick


class ExchangeAdapter(ABC):
    """Base class for exchange market data adapters."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the exchange identifier."""

    @abstractmethod
    def stream_ticks(self, symbols: list[str]) -> AsyncIterator[Tick]:
        """Stream normalized ticks for the given symbols."""

    @abstractmethod
    def stream_candles(self, symbols: list[str], interval: str) -> AsyncIterator[Candle]:
        """Stream normalized candles for the given symbols and interval."""
