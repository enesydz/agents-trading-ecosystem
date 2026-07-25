"""Tests for the Binance adapter normalization logic."""

import pytest

from market_data.adapters.binance import denormalize_symbol, normalize_symbol


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("btcusdt", "BTC-USDT"),
        ("ethbtc", "ETH-BTC"),
        ("solusdc", "SOL-USDC"),
    ],
)
def test_denormalize_symbol(raw: str, expected: str) -> None:
    assert denormalize_symbol(raw) == expected


def test_normalize_symbol_roundtrip() -> None:
    assert normalize_symbol("BTC-USDT") == "btcusdt"
    assert normalize_symbol("ETH-BTC") == "ethbtc"
