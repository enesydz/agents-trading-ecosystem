"""Binance WebSocket market data adapter."""

import json
from collections.abc import AsyncIterator
from datetime import UTC, datetime
from decimal import Decimal

import websockets
from domain_models.market_data import Candle, Tick

from market_data.adapters.base import ExchangeAdapter


def normalize_symbol(symbol: str) -> str:
    """Convert a hyphenated symbol to Binance lowercase format."""
    return symbol.replace("-", "").lower()


def denormalize_symbol(raw: str) -> str:
    """Convert a Binance lowercase symbol back to the normalized form."""
    upper = raw.upper()
    # Stablecoins and common quote assets: insert hyphen before the quote.
    for quote in ["USDT", "BUSD", "USDC", "BTC", "ETH", "FDUSD", "TUSD"]:
        if upper.endswith(quote):
            return f"{upper[: -len(quote)]}-{quote}"
    return upper


class BinanceAdapter(ExchangeAdapter):
    """Binance spot market WebSocket adapter."""

    WS_BASE = "wss://stream.binance.com:9443/ws"

    @property
    def name(self) -> str:
        return "binance"

    def _tick_url(self, symbols: list[str]) -> str:
        streams = "/".join(f"{normalize_symbol(s)}@trade" for s in symbols)
        return f"{self.WS_BASE}/{streams}"

    def _candle_url(self, symbols: list[str], interval: str) -> str:
        streams = "/".join(f"{normalize_symbol(s)}@kline_{interval}" for s in symbols)
        return f"{self.WS_BASE}/{streams}"

    async def stream_ticks(self, symbols: list[str]) -> AsyncIterator[Tick]:
        """Stream aggregate trades as normalized ticks."""
        url = self._tick_url(symbols)
        async with websockets.connect(url) as websocket:
            async for raw_message in websocket:
                data = json.loads(raw_message)
                if data.get("e") != "trade":
                    continue
                yield Tick(
                    symbol=denormalize_symbol(data["s"]),
                    exchange=self.name,
                    timestamp=_from_ms(data["T"]),
                    price=Decimal(data["p"]),
                    volume=Decimal(data["q"]),
                )

    async def stream_candles(self, symbols: list[str], interval: str) -> AsyncIterator[Candle]:
        """Stream kline/candle events."""
        url = self._candle_url(symbols, interval)
        async with websockets.connect(url) as websocket:
            async for raw_message in websocket:
                data = json.loads(raw_message)
                if data.get("e") != "kline":
                    continue
                k = data["k"]
                if not k.get("x", False):
                    # Only emit closed candles to avoid repaints.
                    continue
                yield Candle(
                    symbol=denormalize_symbol(data["s"]),
                    exchange=self.name,
                    interval=k["i"],
                    timestamp=_from_ms(k["t"]),
                    open=Decimal(k["o"]),
                    high=Decimal(k["h"]),
                    low=Decimal(k["l"]),
                    close=Decimal(k["c"]),
                    volume=Decimal(k["v"]),
                )


def _from_ms(ts: int) -> datetime:
    return datetime.fromtimestamp(ts / 1000.0, tz=UTC)
