"""Order domain models."""

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(UTC)


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(str, Enum):
    PENDING = "pending"
    OPEN = "open"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class Order(BaseModel):
    """A normalized trading order."""

    id: str = Field(..., description="Unique order identifier (UUID)")
    symbol: str
    exchange: str
    side: OrderSide
    type: OrderType
    quantity: Decimal = Field(..., gt=0)
    price: Decimal | None = Field(default=None, description="Required for limit orders")
    stop_price: Decimal | None = Field(default=None, description="Required for stop orders")
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)
