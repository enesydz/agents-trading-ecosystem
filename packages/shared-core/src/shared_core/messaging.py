"""Redis Streams implementation of the event bus."""

import json
from collections.abc import Callable, Coroutine
from typing import Any, cast

import redis.asyncio as redis
from domain_models.events import EventEnvelope

from shared_core.events import EventBus

# Redis type stubs are incomplete; cast client to Any for stream operations.
RedisClient = Any


class RedisEventBus(EventBus):
    """Event bus backed by Redis Streams."""

    def __init__(self, redis_client: redis.Redis) -> None:
        self._redis: RedisClient = redis_client

    async def publish(self, stream: str, envelope: EventEnvelope) -> None:
        """Publish an event envelope to a Redis stream."""
        data: dict[str, str] = {
            "metadata": envelope.metadata.model_dump_json(),
            "payload": json.dumps(envelope.payload),
        }
        await self._redis.xadd(stream, cast(Any, data))

    async def subscribe(
        self,
        stream: str,
        consumer_group: str,
        consumer_name: str,
        handler: Callable[[EventEnvelope], Coroutine[Any, Any, None]],
    ) -> None:
        """Subscribe to a Redis stream as part of a consumer group."""
        try:
            await self._redis.xgroup_create(stream, consumer_group, id="0", mkstream=True)
        except redis.ResponseError as exc:
            if "already exists" not in str(exc):
                raise

        while True:
            messages: list[Any] = await self._redis.xreadgroup(
                groupname=consumer_group,
                consumername=consumer_name,
                streams={stream: ">"},
                count=1,
                block=5000,
            )
            for _stream_name, entries in messages:
                entries = cast(list[tuple[str, dict[str, str]]], entries)
                for message_id, fields in entries:
                    envelope = EventEnvelope(
                        metadata=json.loads(fields["metadata"]),
                        payload=json.loads(fields["payload"]),
                    )
                    await handler(envelope)
                    await self._redis.xack(stream, consumer_group, message_id)
