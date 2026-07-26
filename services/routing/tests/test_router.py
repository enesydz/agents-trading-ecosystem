from decimal import Decimal

from routing.router import SmartOrderRouter, VenueQuote


def test_router_accounts_for_fees() -> None:
    quotes = [
        VenueQuote("a", "BTC-USDT", Decimal("99"), Decimal("101"), Decimal("0.01")),
        VenueQuote("b", "BTC-USDT", Decimal("100"), Decimal("102.5"), Decimal("0")),
    ]
    assert SmartOrderRouter().route("buy", quotes).venue == "a"
