"""Portfolio application service."""

from decimal import Decimal

from domain_models.events import EventEnvelope
from domain_models.market_data import Tick
from domain_models.orders import OrderSide
from shared_core.logging import get_logger

from portfolio.domain.position import PortfolioSnapshot, Position

logger = get_logger(__name__)


class PortfolioService:
    """In-memory portfolio tracking service."""

    def __init__(self) -> None:
        self._positions: dict[str, Position] = {}

    def _key(self, symbol: str, exchange: str) -> str:
        return f"{exchange}:{symbol}"

    def get_position(self, symbol: str, exchange: str) -> Position:
        key = self._key(symbol, exchange)
        return self._positions.setdefault(key, Position(symbol=symbol, exchange=exchange))

    def apply_fill(
        self,
        symbol: str,
        exchange: str,
        side: OrderSide,
        quantity: Decimal,
        price: Decimal,
    ) -> None:
        """Apply a fill to the portfolio."""
        position = self.get_position(symbol, exchange)
        position.apply_fill(side.value, quantity, price)
        logger.info(
            "portfolio.fill_applied",
            symbol=symbol,
            exchange=exchange,
            side=side.value,
            quantity=str(quantity),
            price=str(price),
            quantity_after=str(position.quantity),
        )

    def handle_tick(self, envelope: EventEnvelope) -> None:
        """Update unrealized PnL from a market tick."""
        tick = Tick.model_validate(envelope.payload)
        position = self.get_position(tick.symbol, tick.exchange)
        if position.quantity != 0:
            position.mark_to_market(tick.price)

    def snapshot(self) -> PortfolioSnapshot:
        """Return a current portfolio snapshot."""
        return PortfolioSnapshot(
            positions=dict(self._positions),
            total_realized_pnl=Decimal(sum(p.realized_pnl for p in self._positions.values())),
            total_unrealized_pnl=Decimal(sum(p.unrealized_pnl for p in self._positions.values())),
            total_market_value=Decimal(sum(p.market_value for p in self._positions.values())),
        )
