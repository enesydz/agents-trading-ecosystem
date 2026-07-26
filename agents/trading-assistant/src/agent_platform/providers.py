"""Provider contracts and the safe offline reasoning provider."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ReasoningRequest:
    """Structured prompt sent to a reasoning provider."""

    role: str
    question: str
    context: tuple[str, ...]


@dataclass(frozen=True)
class ReasoningResponse:
    """Provider response with explicit confidence and rationale."""

    answer: str
    rationale: tuple[str, ...]
    confidence: float


class LLMProvider(Protocol):
    """Provider-agnostic reasoning contract."""

    async def reason(self, request: ReasoningRequest) -> ReasoningResponse: ...


class DeterministicProvider:
    """Offline provider that never invents unavailable market facts."""

    async def reason(self, request: ReasoningRequest) -> ReasoningResponse:
        context = " ".join(request.context) if request.context else "No stored context."
        return ReasoningResponse(
            answer=f"{request.role}: {request.question} Context: {context}",
            rationale=("Response generated from supplied structured context only.",),
            confidence=0.2 if not request.context else 0.5,
        )
