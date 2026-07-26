"""Trading signal domain model."""

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class SignalDirection(str, Enum):
    LONG = "long"
    SHORT = "short"


class Signal(BaseModel):
    """A generated trading signal."""

    symbol: str
    exchange: str
    direction: SignalDirection
    confidence: Decimal = Field(..., ge=0, le=1, description="Confidence score 0-1")
    quantity: Decimal = Field(default=Decimal("0.01"), gt=0)
    strategy: str = Field(..., description="Strategy identifier that produced the signal")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, str | int | float | bool] = Field(default_factory=dict)
