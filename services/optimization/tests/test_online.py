from decimal import Decimal

from optimization.online import OnlineOptimizer


def test_optimizer_requires_evidence_before_recommendation() -> None:
    optimizer = OnlineOptimizer(min_observations=2)
    optimizer.observe("sma", "v1", Decimal("0.1"))
    assert optimizer.recommend("sma") is None
    optimizer.observe("sma", "v1", Decimal("0.2"))
    assert optimizer.recommend("sma").version == "v1"
