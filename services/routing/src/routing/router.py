"""Deterministic best-venue routing with fee and slippage awareness."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class VenueQuote:
    """Executable quote from one venue."""

    venue: str
    symbol: str
    bid: Decimal
    ask: Decimal
    fee_rate: Decimal = Decimal(0)


class SmartOrderRouter:
    """Selects the cheapest effective ask or highest effective bid."""

    def route(self, side: str, quotes: list[VenueQuote]) -> VenueQuote:
        if side not in {"buy", "sell"}:
            raise ValueError("side must be buy or sell")
        if not quotes:
            raise ValueError("at least one quote is required")
        if side == "buy":
            return min(quotes, key=lambda quote: quote.ask * (1 + quote.fee_rate))
        return max(quotes, key=lambda quote: quote.bid * (1 - quote.fee_rate))

    def arbitrage(self, quotes: list[VenueQuote]) -> tuple[VenueQuote, VenueQuote] | None:
        """Return buy/sell venues only when a positive fee-adjusted edge exists."""
        if len(quotes) < 2:
            return None
        buy = min(quotes, key=lambda quote: quote.ask * (1 + quote.fee_rate))
        sell = max(quotes, key=lambda quote: quote.bid * (1 - quote.fee_rate))
        if sell.bid * (1 - sell.fee_rate) > buy.ask * (1 + buy.fee_rate):
            return buy, sell
        return None
