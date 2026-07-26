"""Tests for offline agent orchestration."""

import pytest
from agent_platform.assistant import MarketAnalyst, TradingAssistant
from agent_platform.evaluation import evaluate
from agent_platform.memory import InMemoryMemory
from agent_platform.orchestrator import AgentOrchestrator
from agent_platform.providers import DeterministicProvider
from agent_platform.tools import ToolRegistry, ToolSpec


@pytest.mark.asyncio
async def test_orchestrator_produces_grounded_auditable_response() -> None:
    memory = InMemoryMemory()
    memory.remember("1", "BTC liquidity swept above resistance", "market-event:1")
    provider = DeterministicProvider()
    orchestrator = AgentOrchestrator(
        TradingAssistant(provider, memory), MarketAnalyst(provider, memory)
    )
    result = await orchestrator.ask("BTC liquidity")
    evaluation = evaluate(result)
    assert evaluation.grounded
    assert evaluation.score == 1
    assert len(orchestrator.events()) == 1


@pytest.mark.asyncio
async def test_live_tool_is_blocked_by_default() -> None:
    registry = ToolRegistry()

    async def place_order(**_: object) -> dict[str, object]:
        return {"accepted": True}

    registry.register(ToolSpec("place_order", "Place an order", place_order, paper_only=False))
    with pytest.raises(PermissionError):
        await registry.call("place_order")
