"""Event envelope and metadata models."""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(UTC)


class EventMetadata(BaseModel):
    """Metadata attached to every event."""

    event_id: str = Field(..., description="Unique event identifier")
    event_type: str = Field(..., description="Domain event type, e.g., MarketTick")
    source: str = Field(..., description="Service or agent that produced the event")
    correlation_id: str | None = Field(None, description="Request/trace correlation id")
    produced_at: datetime = Field(default_factory=_utc_now)
    schema_version: str = "1.0"


class EventEnvelope(BaseModel):
    """Wrapper for all domain events."""

    metadata: EventMetadata
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        event_type: str,
        source: str,
        payload: dict[str, Any],
        event_id: str,
        correlation_id: str | None = None,
    ) -> "EventEnvelope":
        """Factory for creating a validated event envelope."""
        """Factory for creating a validated event envelope."""
        return cls(
            metadata=EventMetadata(
                event_id=event_id,
                event_type=event_type,
                source=source,
                correlation_id=correlation_id,
            ),
            payload=payload,
        )
