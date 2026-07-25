"""Market data API routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/market")


@router.get("/symbols")
async def list_symbols() -> list[str]:
    """Return the list of tracked symbols."""
    return ["BTC-USDT", "ETH-USDT"]
