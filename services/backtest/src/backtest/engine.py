"""Deterministic event-driven backtest engine."""

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal

from domain_models.market_data import Candle
from strategy.domain.signal import SignalDirection
from strategy.domain.strategy import Strategy

from backtest.analytics import PerformanceReport, build_report


@dataclass(frozen=True)
class BacktestTrade:
    """A simulated entry or reversal executed at candle close."""

    symbol: str
    direction: SignalDirection
    quantity: Decimal
    price: Decimal
    timestamp: object
    pnl: Decimal = Decimal(0)


class BacktestEngine:
    """Feeds candles to a strategy and simulates one position per symbol."""

    def __init__(self, strategy: Strategy, initial_equity: Decimal = Decimal("10000")) -> None:
        if initial_equity <= 0:
            raise ValueError("initial_equity must be positive")
        self._strategy = strategy
        self._initial_equity = initial_equity

    def run(self, candles: Iterable[Candle]) -> PerformanceReport:
        trades: list[BacktestTrade] = []
        positions: dict[str, tuple[SignalDirection, Decimal, Decimal]] = {}
        equity_curve: list[Decimal] = [self._initial_equity]
        history: list[Candle] = []

        for candle in candles:
            signal = self._strategy.on_candle(candle, history=tuple(history))
            history.append(candle)
            if signal is None:
                equity_curve.append(self._mark_equity(positions, candle, equity_curve[-1]))
                continue

            previous = positions.pop(signal.symbol, None)
            realized = Decimal(0)
            if previous is not None:
                old_direction, quantity, entry = previous
                sign = Decimal(1) if old_direction == SignalDirection.LONG else Decimal(-1)
                realized = (candle.close - entry) * quantity * sign
                trades.append(
                    BacktestTrade(
                        symbol=signal.symbol,
                        direction=old_direction,
                        quantity=quantity,
                        price=candle.close,
                        timestamp=candle.timestamp,
                        pnl=realized,
                    )
                )
            positions[signal.symbol] = (signal.direction, signal.quantity, candle.close)
            equity_curve.append(equity_curve[-1] + realized)

        if history:
            final = history[-1]
            for symbol, (direction, quantity, entry) in positions.items():
                if symbol == final.symbol:
                    sign = Decimal(1) if direction == SignalDirection.LONG else Decimal(-1)
                    trades.append(
                        BacktestTrade(
                            symbol=symbol,
                            direction=direction,
                            quantity=quantity,
                            price=final.close,
                            timestamp=final.timestamp,
                            pnl=(final.close - entry) * quantity * sign,
                        )
                    )
        return build_report(self._initial_equity, equity_curve, trades)

    @staticmethod
    def _mark_equity(
        positions: dict[str, tuple[SignalDirection, Decimal, Decimal]],
        candle: Candle,
        equity: Decimal,
    ) -> Decimal:
        position = positions.get(candle.symbol)
        if position is None:
            return equity
        direction, quantity, entry = position
        sign = Decimal(1) if direction == SignalDirection.LONG else Decimal(-1)
        return equity + (candle.close - entry) * quantity * sign
