"""Event-oriented agent orchestration and audit trail."""

from dataclasses import dataclass
from datetime import UTC, datetime

from agent_platform.assistant import AgentResult, MarketAnalyst, TradingAssistant


@dataclass(frozen=True)
class AgentEvent:
    """An auditable request/result event."""

    event_type: str
    agent: str
    payload: dict[str, object]
    timestamp: datetime


class AgentOrchestrator:
    """Routes named agent jobs and retains a local audit trail."""

    def __init__(self, assistant: TradingAssistant, analyst: MarketAnalyst) -> None:
        self._assistant = assistant
        self._analyst = analyst
        self._events: list[AgentEvent] = []

    async def ask(self, question: str) -> AgentResult:
        result = await self._assistant.answer(question)
        self._record(result)
        return result

    async def analyze(self, symbol: str, observations: list[str]) -> AgentResult:
        result = await self._analyst.analyze(symbol, observations)
        self._record(result)
        return result

    def events(self) -> tuple[AgentEvent, ...]:
        return tuple(self._events)

    def _record(self, result: AgentResult) -> None:
        self._events.append(
            AgentEvent(
                event_type="AgentResponse",
                agent=result.agent,
                payload={
                    "answer": result.response.answer,
                    "confidence": result.response.confidence,
                },
                timestamp=datetime.now(UTC),
            )
        )
