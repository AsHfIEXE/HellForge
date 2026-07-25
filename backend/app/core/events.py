import asyncio
import logging
from typing import Dict, List, Callable, Any, Awaitable

logger = logging.getLogger("HellForge.TopicEventBus")

class TopicChannel:
    def __init__(self, channel_name: str):
        self.name = channel_name
        self._subscribers: List[Callable[[Any], Awaitable[None]]] = []

    def subscribe(self, callback: Callable[[Any], Awaitable[None]]):
        self._subscribers.append(callback)
        logger.info(f"Subscribed callback to channel '{self.name}'")

    async def publish(self, data: Any):
        tasks = [asyncio.create_task(sub(data)) for sub in self._subscribers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

class EventBusManager:
    """
    Split Topic Event Bus Architecture.
    Prevents event flooding across unrelated plugins.
    """
    def __init__(self):
        self.scan_bus = TopicChannel("scan")
        self.asset_bus = TopicChannel("asset")
        self.http_bus = TopicChannel("http")
        self.finding_bus = TopicChannel("finding")
        self.risk_bus = TopicChannel("risk")
        self.system_bus = TopicChannel("system")

        self.channels = {
            "scan": self.scan_bus,
            "asset": self.asset_bus,
            "http": self.http_bus,
            "finding": self.finding_bus,
            "risk": self.risk_bus,
            "system": self.system_bus
        }

    def get_channel(self, name: str) -> TopicChannel:
        return self.channels.get(name, self.system_bus)

event_bus_manager = EventBusManager()
