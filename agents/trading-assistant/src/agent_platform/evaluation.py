"""Simple deterministic evaluation pipeline for agent outputs."""

from dataclasses import dataclass

from agent_platform.assistant import AgentResult


@dataclass(frozen=True)
class EvaluationResult:
    """Evaluation score and safety findings."""

    grounded: bool
    has_rationale: bool
    score: float
    findings: tuple[str, ...]


def evaluate(result: AgentResult) -> EvaluationResult:
    """Check grounding, rationale, confidence bounds, and empty responses."""
    findings: list[str] = []
    grounded = bool(result.citations) or "No stored context" in result.response.answer
    if not grounded:
        findings.append("response has no traceable context")
    has_rationale = bool(result.response.rationale)
    if not has_rationale:
        findings.append("response has no rationale")
    if not 0 <= result.response.confidence <= 1:
        findings.append("confidence is outside [0, 1]")
    if not result.response.answer.strip():
        findings.append("response is empty")
    score = (float(grounded) + float(has_rationale) + float(not findings)) / 3
    return EvaluationResult(grounded, has_rationale, score, tuple(findings))
