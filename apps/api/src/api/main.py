"""API Gateway entry point."""

from fastapi import FastAPI

from api.health import router as health_router
from api.routes import market, portfolio

app = FastAPI(
    title="Agents Trading Ecosystem API",
    description="API Gateway for market data, orders, and agent interactions.",
    version="0.1.0",
)

app.include_router(health_router, tags=["Health"])
app.include_router(market.router, tags=["Market Data"])
app.include_router(portfolio.router, tags=["Portfolio"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Agents Trading Ecosystem API"}
