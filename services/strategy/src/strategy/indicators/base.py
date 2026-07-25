"""Indicator plugin abstractions."""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import ClassVar

from domain_models.market_data import Candle


class Indicator(ABC):
    """Base class for technical indicators."""

    name: ClassVar[str]

    @abstractmethod
    def update(self, candle: Candle) -> None:
        """Feed a new closed candle into the indicator."""

    @abstractmethod
    def value(self) -> Decimal | None:
        """Return the current indicator value, or None if not ready."""

    @abstractmethod
    def reset(self) -> None:
        """Reset the indicator state."""


class IndicatorRegistry:
    """Registry for indicator plugins."""

    def __init__(self) -> None:
        self._indicators: dict[str, type[Indicator]] = {}

    def register(self, indicator_cls: type[Indicator]) -> type[Indicator]:
        """Register an indicator class."""
        self._indicators[indicator_cls.name] = indicator_cls
        return indicator_cls

    def get(self, name: str) -> type[Indicator]:
        """Return the indicator class by name."""
        if name not in self._indicators:
            raise KeyError(f"Indicator '{name}' is not registered")
        return self._indicators[name]

    def build(self, name: str, **params: object) -> Indicator:
        """Instantiate an indicator by name with parameters."""
        cls = self.get(name)
        return cls(**params)

    def list_indicators(self) -> Sequence[str]:
        """Return all registered indicator names."""
        return sorted(self._indicators.keys())
