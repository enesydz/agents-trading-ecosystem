"""Tests for live execution safety defaults."""

from decimal import Decimal

import pytest
from domain_models.orders import Order, OrderSide, OrderType

from execution.domain.live_adapter import DryRunLiveAdapter


def _order() -> Order:
    return Order(
        id="test-order", symbol="BTC-USDT", exchange="binance", side=OrderSide.BUY,
        type=OrderType.MARKET, quantity=Decimal("0.01")
    )


@pytest.mark.asyncio
async def test_live_adapter_fails_closed_until_explicitly_enabled() -> None:
    adapter = DryRunLiveAdapter()
    blocked = await adapter.submit(_order())
    assert not blocked.accepted
    with pytest.raises(ValueError):
        adapter.enable("yes")
    adapter.enable("ENABLE_LIVE_TRADING")
    result = await adapter.submit(_order())
    assert result.accepted
