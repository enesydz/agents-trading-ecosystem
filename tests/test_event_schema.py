"""Sanity tests for the shared event schema."""

from domain_models.events import EventEnvelope
from domain_models.market_data import Tick


def test_tick_event_roundtrip() -> None:
    tick = Tick(
        symbol="BTC-USD",
        exchange="example",
        price="100.00",
        volume="0.5",
    )
    envelope = EventEnvelope.create(
        event_type="MarketTick",
        source="market-data",
        payload=tick.model_dump(mode="json"),
        event_id="evt-1",
        correlation_id="corr-1",
    )
    assert envelope.metadata.event_type == "MarketTick"
    assert envelope.payload["symbol"] == "BTC-USD"
    assert envelope.metadata.correlation_id == "corr-1"
