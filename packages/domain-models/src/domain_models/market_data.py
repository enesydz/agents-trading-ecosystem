"""Market data domain models."""

from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(UTC)


class Tick(BaseModel):
    """A normalized market tick."""

    symbol: str = Field(..., description="Trading pair or instrument symbol")
    exchange: str = Field(..., description="Source exchange")
    timestamp: datetime = Field(default_factory=_utc_now, description="Exchange timestamp in UTC")
    received_at: datetime = Field(default_factory=_utc_now, description="Local receipt time")
    price: Decimal = Field(..., description="Last traded price")
    volume: Decimal = Field(..., description="Last traded volume")


class Candle(BaseModel):
    """A normalized OHLCV candle."""

    symbol: str
    exchange: str
    interval: str = Field(..., description="Candle interval, e.g., 1m, 5m, 1h")
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    timestamp: datetime = Field(
        default_factory=_utc_now, description="Candle open timestamp in UTC"
    )
    received_at: datetime = Field(default_factory=_utc_now)
