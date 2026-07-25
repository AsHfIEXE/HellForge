import abc
import yaml
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.core.events import event_bus_manager
from app.core.dtos import ScanContext

class PluginManifest(BaseModel):
    name: str
    version: str = "1.0.0"
    author: str = "Community"
    description: str = ""
    subscriptions: List[str] = [] # e.g. ["scan", "asset", "http"]

class BasePlugin(abc.ABC):
    """
    Refined Plugin SDK interface supporting complete lifecycle and manifest metadata.
    """
    def __init__(self, manifest_path: Optional[str] = None):
        self.manifest: Optional[PluginManifest] = None
        if manifest_path and os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                data = yaml.safe_load(f)
                self.manifest = PluginManifest(**data)
        
        self.name = self.manifest.name if self.manifest else getattr(self, 'name', 'BasePlugin')
        self.version = self.manifest.version if self.manifest else getattr(self, 'version', '1.0.0')
        self.subscriptions = self.manifest.subscriptions if self.manifest else getattr(self, 'subscriptions', [])

    async def initialize(self, ctx: ScanContext):
        """Subscribe to topic buses based on manifest subscriptions."""
        for sub_topic in self.subscriptions:
            channel = event_bus_manager.get_channel(sub_topic)
            channel.subscribe(self.execute)

    async def configure(self, config: Dict[str, Any]):
        pass

    @abc.abstractmethod
    async def execute(self, event_data: Any):
        pass

    async def cleanup(self):
        pass

    async def shutdown(self):
        pass

    async def on_error(self, error: Exception):
        pass

    async def health_check(self) -> bool:
        return True
