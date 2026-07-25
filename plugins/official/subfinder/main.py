import os
import asyncio
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus_manager
from app.core.dtos import ScanContext, AssetEvent

class SubfinderPlugin(BasePlugin):
    def __init__(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "plugin.yaml")
        super().__init__(manifest_path)

    async def execute(self, event_data: Any):
        if isinstance(event_data, ScanContext):
            domain = event_data.target_domain
            await asyncio.sleep(0.2)
            
            subs = [
                f"api.{domain}",
                f"admin.{domain}",
                f"dev.{domain}",
                f"auth.{domain}",
                f"vpn.{domain}"
            ]
            
            for sub in subs:
                asset_evt = AssetEvent(
                    scan_id=event_data.scan_id,
                    domain=domain,
                    subdomain=sub,
                    tags=["subdomain", "passive"],
                    discovery_source="subfinder"
                )
                # Publish to asset_bus topic channel
                await event_bus_manager.asset_bus.publish(asset_evt)
