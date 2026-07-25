"""Position and portfolio domain models."""

from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Position(BaseModel):
    """A position in a single instrument."""

    symbol: str
    exchange: str
    quantity: Decimal = Field(default=Decimal(0), description="Positive long, negative short")
    average_entry: Decimal = Field(default=Decimal(0))
    realized_pnl: Decimal = Field(default=Decimal(0))
    unrealized_pnl: Decimal = Field(default=Decimal(0))
    last_price: Decimal | None = Field(default=None)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def market_value(self) -> Decimal:
        if self.last_price is None:
            return Decimal(0)
        return self.quantity * self.last_price

    def apply_fill(self, side: str, quantity: Decimal, price: Decimal) -> None:
        """Update the position based on an execution fill."""
        signed_qty = quantity if side == "buy" else -quantity
        new_qty = self.quantity + signed_qty

        # Closing/reducing portion realizes PnL for the opposing quantity.
        if self.quantity != 0 and (new_qty == 0 or (self.quantity > 0) != (signed_qty > 0)):
            reduce_qty = min(self.quantity.copy_abs(), quantity)
            direction = 1 if self.quantity > 0 else -1
            self.realized_pnl += direction * (price - self.average_entry) * reduce_qty

        # Update average entry for opening/increasing quantity.
        if new_qty == 0:
            self.average_entry = Decimal(0)
        elif self.quantity == 0 or (self.quantity > 0) == (signed_qty > 0):
            total_cost = self.quantity * self.average_entry + signed_qty * price
            self.average_entry = total_cost / new_qty
        else:
            self.average_entry = self.average_entry  # reduced only

        self.quantity = new_qty
        self.last_price = price
        self.last_updated = datetime.now(UTC)

    def mark_to_market(self, price: Decimal) -> None:
        """Update unrealized PnL based on the latest market price."""
        self.last_price = price
        if self.quantity == 0 or self.average_entry == 0:
            self.unrealized_pnl = Decimal(0)
        else:
            self.unrealized_pnl = (price - self.average_entry) * self.quantity
        self.last_updated = datetime.now(UTC)


class PortfolioSnapshot(BaseModel):
    """Snapshot of the entire portfolio."""

    positions: dict[str, Position]
    total_realized_pnl: Decimal
    total_unrealized_pnl: Decimal
    total_market_value: Decimal
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
