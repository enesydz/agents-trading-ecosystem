"""Event bus abstractions and domain event base class."""

from abc import ABC, abstractmethod
from typing import Any
from uuid import uuid4

from domain_models.events import EventEnvelope, EventMetadata


class DomainEvent(ABC):
    """Base class for all domain events."""

    event_type: str
    source: str

    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def to_envelope(self, correlation_id: str | None = None) -> EventEnvelope:
        """Serialize the event into an envelope."""
        return EventEnvelope(
            metadata=EventMetadata(
                event_id=str(uuid4()),
                event_type=self.event_type,
                source=self.source,
                correlation_id=correlation_id,
            ),
            payload=self.payload,
        )


class EventBus(ABC):
    """Abstract event bus for publishing and subscribing to domain events."""

    @abstractmethod
    async def publish(self, stream: str, envelope: EventEnvelope) -> None:
        """Publish an event envelope to a stream."""

    @abstractmethod
    async def subscribe(
        self,
        stream: str,
        consumer_group: str,
        consumer_name: str,
        handler: Any,
    ) -> None:
        """Subscribe to a stream with a consumer group."""
