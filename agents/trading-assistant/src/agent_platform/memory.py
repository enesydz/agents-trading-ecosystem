"""Small, deterministic memory/RAG layer with injectable persistence."""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


@dataclass(frozen=True)
class MemoryRecord:
    """A searchable event or document fragment."""

    record_id: str
    text: str
    source: str
    metadata: dict[str, str]
    created_at: datetime


class MemoryStore(Protocol):
    """Persistence contract for agent memory."""

    def add(self, record: MemoryRecord) -> None: ...

    def search(self, query: str, limit: int = 5) -> list[MemoryRecord]: ...


class InMemoryMemory:
    """Offline lexical memory used in development and tests."""

    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def add(self, record: MemoryRecord) -> None:
        self._records.append(record)

    def search(self, query: str, limit: int = 5) -> list[MemoryRecord]:
        terms = set(query.lower().split())
        ranked = sorted(
            self._records,
            key=lambda record: len(terms & set(record.text.lower().split())),
            reverse=True,
        )
        return [record for record in ranked if terms & set(record.text.lower().split())][:limit]

    def remember(self, record_id: str, text: str, source: str, **metadata: str) -> None:
        self.add(
            MemoryRecord(
                record_id=record_id,
                text=text,
                source=source,
                metadata=metadata,
                created_at=datetime.now(UTC),
            )
        )
