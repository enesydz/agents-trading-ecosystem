"""Fill domain model."""

from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Fill(BaseModel):
    """A single execution fill."""

    order_id: str
    symbol: str
    exchange: str
    side: str
    quantity: Decimal
    price: Decimal
    fee: Decimal = Decimal(0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
