"""Tests for position and portfolio calculations."""

from decimal import Decimal

from domain_models.orders import OrderSide

from portfolio.application.service import PortfolioService


def test_buy_fill_opens_long_position() -> None:
    service = PortfolioService()
    service.apply_fill("BTC-USDT", "binance", OrderSide.BUY, Decimal("0.5"), Decimal(100))
    position = service.get_position("BTC-USDT", "binance")

    assert position.quantity == Decimal("0.5")
    assert position.average_entry == Decimal(100)


def test_sell_fill_reduces_long_position() -> None:
    service = PortfolioService()
    service.apply_fill("BTC-USDT", "binance", OrderSide.BUY, Decimal(1), Decimal(100))
    service.apply_fill("BTC-USDT", "binance", OrderSide.SELL, Decimal("0.5"), Decimal(110))
    position = service.get_position("BTC-USDT", "binance")

    assert position.quantity == Decimal("0.5")
    assert position.realized_pnl == Decimal(5)
