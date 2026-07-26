"""Performance analytics for backtest results."""

from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backtest.engine import BacktestTrade


@dataclass(frozen=True)
class PerformanceReport:
    """Summary metrics and the underlying equity curve/trades."""

    initial_equity: Decimal
    final_equity: Decimal
    total_return: Decimal
    max_drawdown: Decimal
    win_rate: Decimal
    trade_count: int
    equity_curve: tuple[Decimal, ...]
    trades: tuple["BacktestTrade", ...]


def build_report(
    initial_equity: Decimal,
    equity_curve: list[Decimal],
    trades: list["BacktestTrade"],
) -> PerformanceReport:
    """Build stable, decimal-based performance metrics."""
    final_equity = equity_curve[-1] if equity_curve else initial_equity
    peak = initial_equity
    max_drawdown = Decimal(0)
    for equity in equity_curve:
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, peak - equity)
    closed = [trade for trade in trades if trade.pnl != 0]
    wins = sum(1 for trade in closed if trade.pnl > 0)
    return PerformanceReport(
        initial_equity=initial_equity,
        final_equity=final_equity,
        total_return=(final_equity - initial_equity) / initial_equity,
        max_drawdown=max_drawdown,
        win_rate=Decimal(wins) / Decimal(len(closed)) if closed else Decimal(0),
        trade_count=len(trades),
        equity_curve=tuple(equity_curve),
        trades=tuple(trades),
    )
