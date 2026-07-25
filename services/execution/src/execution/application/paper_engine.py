"""Paper trading execution engine."""

from decimal import Decimal
from uuid import uuid4

from domain_models.events import EventEnvelope
from domain_models.market_data import Tick
from domain_models.orders import Order, OrderSide, OrderStatus, OrderType
from shared_core.events import EventBus
from shared_core.logging import get_logger

from execution.domain.fill import Fill

logger = get_logger(__name__)


class PaperExecutionEngine:
    """Simulates order execution at the latest market price."""

    FILL_STREAM = "execution:fills"

    def __init__(self, event_bus: EventBus) -> None:
        self._bus = event_bus
        self._orders: dict[str, Order] = {}
        self._latest_prices: dict[str, Decimal] = {}

    def _price_key(self, symbol: str, exchange: str) -> str:
        return f"{exchange}:{symbol}"

    async def handle_signal(self, envelope: EventEnvelope) -> None:
        """Convert a SignalGenerated event into a paper order."""
        payload = envelope.payload
        direction = payload["direction"]
        side = OrderSide.BUY if direction == "long" else OrderSide.SELL
        symbol = payload["symbol"]
        exchange = payload["exchange"]

        order = Order(
            id=str(uuid4()),
            symbol=symbol,
            exchange=exchange,
            side=side,
            type=OrderType.MARKET,
            quantity=Decimal("0.01"),  # Fixed paper size for early testing
        )
        self._orders[order.id] = order
        logger.info(
            "paper_order.created",
            order_id=order.id,
            symbol=symbol,
            side=side.value,
            quantity=str(order.quantity),
        )
        await self._try_fill(order)

    async def handle_tick(self, envelope: EventEnvelope) -> None:
        """Update latest prices and attempt to fill pending market orders."""
        tick = Tick.model_validate(envelope.payload)
        key = self._price_key(tick.symbol, tick.exchange)
        self._latest_prices[key] = tick.price

        for order in list(self._orders.values()):
            if order.status == OrderStatus.PENDING:
                await self._try_fill(order)

    async def _try_fill(self, order: Order) -> None:
        key = self._price_key(order.symbol, order.exchange)
        price = self._latest_prices.get(key)
        if price is None:
            return

        order.status = OrderStatus.FILLED
        fill = Fill(
            order_id=order.id,
            symbol=order.symbol,
            exchange=order.exchange,
            side=order.side.value,
            quantity=order.quantity,
            price=price,
        )
        logger.info(
            "paper_order.filled",
            order_id=order.id,
            symbol=order.symbol,
            side=order.side.value,
            quantity=str(order.quantity),
            price=str(price),
        )
        await self._publish_fill(fill)

    async def _publish_fill(self, fill: Fill) -> None:
        envelope = EventEnvelope.create(
            event_type="OrderFilled",
            source="paper-execution-engine",
            payload=fill.model_dump(mode="json"),
            event_id=str(uuid4()),
        )
        await self._bus.publish(self.FILL_STREAM, envelope)
