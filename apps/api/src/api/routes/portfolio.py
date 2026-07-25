"""Portfolio API routes."""

from decimal import Decimal
from typing import Any

from fastapi import APIRouter
from portfolio.application.service import PortfolioService

router = APIRouter(prefix="/portfolio")


def _decimal_to_str(value: Decimal) -> str:
    return str(value)


@router.get("/snapshot")
async def portfolio_snapshot() -> dict[str, Any]:
    """Return the current portfolio snapshot."""
    service = PortfolioService()
    snapshot = service.snapshot()
    return {
        "timestamp": snapshot.timestamp.isoformat(),
        "total_realized_pnl": _decimal_to_str(snapshot.total_realized_pnl),
        "total_unrealized_pnl": _decimal_to_str(snapshot.total_unrealized_pnl),
        "total_market_value": _decimal_to_str(snapshot.total_market_value),
        "positions": [
            {
                "symbol": pos.symbol,
                "exchange": pos.exchange,
                "quantity": _decimal_to_str(pos.quantity),
                "average_entry": _decimal_to_str(pos.average_entry),
                "realized_pnl": _decimal_to_str(pos.realized_pnl),
                "unrealized_pnl": _decimal_to_str(pos.unrealized_pnl),
                "last_price": _decimal_to_str(pos.last_price) if pos.last_price else None,
            }
            for pos in snapshot.positions.values()
        ],
    }
