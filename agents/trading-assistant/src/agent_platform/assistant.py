"""Trading assistant and market analyst agents."""

from dataclasses import dataclass

from agent_platform.memory import MemoryStore
from agent_platform.providers import LLMProvider, ReasoningRequest, ReasoningResponse


@dataclass(frozen=True)
class AgentResult:
    """Auditable agent output."""

    agent: str
    response: ReasoningResponse
    citations: tuple[str, ...]


class TradingAssistant:
    """Answers operator questions using structured memory context."""

    name = "trading-assistant"

    def __init__(self, provider: LLMProvider, memory: MemoryStore) -> None:
        self._provider = provider
        self._memory = memory

    async def answer(self, question: str) -> AgentResult:
        memories = self._memory.search(question)
        response = await self._provider.reason(
            ReasoningRequest("Trading assistant", question, tuple(item.text for item in memories))
        )
        return AgentResult(self.name, response, tuple(item.source for item in memories))


class MarketAnalyst:
    """Produces a narrative from supplied market structure observations."""

    name = "market-analyst"

    def __init__(self, provider: LLMProvider, memory: MemoryStore) -> None:
        self._provider = provider
        self._memory = memory

    async def analyze(self, symbol: str, observations: list[str]) -> AgentResult:
        query = f"{symbol} market structure"
        memories = self._memory.search(query)
        response = await self._provider.reason(
            ReasoningRequest(
                "Market analyst", query, tuple(observations) + tuple(item.text for item in memories)
            )
        )
        return AgentResult(self.name, response, tuple(item.source for item in memories))
