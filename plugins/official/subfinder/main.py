import os
import asyncio
import socket
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
            wordlist = ["www", "api", "admin", "dev", "staging", "mail", "vpn", "auth", "portal", "test"]
            discovered = set()
            discovered.add(domain)

            loop = asyncio.get_event_loop()

            for prefix in wordlist:
                candidate = f"{prefix}.{domain}"
                try:
                    ip = await loop.run_in_executor(None, socket.gethostbyname, candidate)
                    discovered.add(candidate)
                except Exception:
                    pass

            for sub in discovered:
                try:
                    resolved_ip = await loop.run_in_executor(None, socket.gethostbyname, sub)
                except Exception:
                    resolved_ip = "127.0.0.1"

                asset_evt = AssetEvent(
                    scan_id=event_data.scan_id,
                    domain=domain,
                    subdomain=sub,
                    ip_address=resolved_ip,
                    tags=["subdomain", "dns-resolved"],
                    discovery_source="subfinder"
                )
                await event_bus_manager.asset_bus.publish(asset_evt)
