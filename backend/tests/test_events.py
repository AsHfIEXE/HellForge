import pytest
import asyncio
from app.core.events import EventBusManager

@pytest.mark.asyncio
async def test_topic_event_bus_publishing():
    manager = EventBusManager()
    received_assets = []

    async def sample_handler(data):
        received_assets.append(data)

    manager.asset_bus.subscribe(sample_handler)
    await manager.asset_bus.publish("test_subdomain_data")

    assert len(received_assets) == 1
    assert received_assets[0] == "test_subdomain_data"

@pytest.mark.asyncio
async def test_topic_isolation():
    manager = EventBusManager()
    finding_received = []

    async def finding_handler(data):
        finding_received.append(data)

    manager.finding_bus.subscribe(finding_handler)
    # Publish to asset_bus, finding_bus should NOT receive it
    await manager.asset_bus.publish("asset_only_payload")

    assert len(finding_received) == 0
