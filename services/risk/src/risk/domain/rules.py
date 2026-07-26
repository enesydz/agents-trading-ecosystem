"""Risk rule abstractions and built-in rules."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from strategy.domain.signal import Signal


@dataclass(frozen=True)
class RiskResult:
    """Outcome of a risk check."""

    passed: bool
    rule: str
    message: str


class RiskRule(ABC):
    """Base class for risk rules."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the rule identifier."""

    @abstractmethod
    def check(self, signal: Signal, context: "RiskContext") -> RiskResult:
        """Evaluate the signal against the rule."""


@dataclass
class RiskContext:
    """Runtime risk context for a signal."""

    daily_pnl: Decimal = Decimal(0)
    daily_loss_limit: Decimal = Decimal(-1000)
    max_position_size: Decimal = Decimal("1.0")
    max_total_exposure: Decimal = Decimal("10.0")
    current_exposure: Decimal = Decimal(0)
    max_drawdown: Decimal = Decimal(1000)
    peak_equity: Decimal = Decimal(0)
    current_equity: Decimal = Decimal(0)
    kill_switch_active: bool = False


class KillSwitchRule(RiskRule):
    """Rejects all signals if the kill switch is active."""

    @property
    def name(self) -> str:
        return "kill_switch"

    def check(self, signal: Signal, context: RiskContext) -> RiskResult:
        if context.kill_switch_active:
            return RiskResult(passed=False, rule=self.name, message="Kill switch is active")
        return RiskResult(passed=True, rule=self.name, message="OK")


class DailyLossLimitRule(RiskRule):
    """Rejects signals if daily loss limit is breached."""

    @property
    def name(self) -> str:
        return "daily_loss_limit"

    def check(self, signal: Signal, context: RiskContext) -> RiskResult:
        if context.daily_pnl <= context.daily_loss_limit:
            return RiskResult(
                passed=False,
                rule=self.name,
                message=f"Daily loss limit reached: {context.daily_pnl}",
            )
        return RiskResult(passed=True, rule=self.name, message="OK")


class PositionSizeRule(RiskRule):
    """Rejects signals that exceed the maximum position size."""

    @property
    def name(self) -> str:
        return "max_position_size"

    def check(self, signal: Signal, context: RiskContext) -> RiskResult:
        if signal.quantity > context.max_position_size:
            return RiskResult(
                passed=False,
                rule=self.name,
                message=f"Position size {signal.quantity} exceeds {context.max_position_size}",
            )
        if context.current_exposure + signal.quantity > context.max_total_exposure:
            return RiskResult(
                passed=False,
                rule=self.name,
                message="Maximum total exposure would be exceeded",
            )
        return RiskResult(passed=True, rule=self.name, message="OK")


class MaxDrawdownRule(RiskRule):
    """Rejects signals after the configured equity drawdown is breached."""

    @property
    def name(self) -> str:
        return "max_drawdown"

    def check(self, signal: Signal, context: RiskContext) -> RiskResult:
        drawdown = context.peak_equity - context.current_equity
        if context.peak_equity > 0 and drawdown >= context.max_drawdown:
            return RiskResult(
                passed=False,
                rule=self.name,
                message=f"Maximum drawdown reached: {drawdown}",
            )
        return RiskResult(passed=True, rule=self.name, message="OK")
