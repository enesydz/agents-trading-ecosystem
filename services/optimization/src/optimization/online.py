"""Conservative online strategy selection and improvement records."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class StrategyScore:
    """Observed score for one strategy version."""

    strategy: str
    version: str
    observations: int = 0
    total_return: Decimal = Decimal(0)

    @property
    def mean_return(self) -> Decimal:
        return self.total_return / self.observations if self.observations else Decimal(0)


class OnlineOptimizer:
    """Selects proven variants and never promotes without a minimum sample size."""

    def __init__(self, min_observations: int = 20) -> None:
        self.min_observations = min_observations
        self._scores: dict[tuple[str, str], StrategyScore] = {}

    def observe(self, strategy: str, version: str, result: Decimal) -> None:
        score = self._scores.setdefault((strategy, version), StrategyScore(strategy, version))
        score.observations += 1
        score.total_return += result

    def recommend(self, strategy: str) -> StrategyScore | None:
        candidates = [
            score for score in self._scores.values()
            if score.strategy == strategy and score.observations >= self.min_observations
        ]
        return max(candidates, key=lambda score: score.mean_return, default=None)

    def scores(self) -> tuple[StrategyScore, ...]:
        return tuple(self._scores.values())
