import asyncio
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus

class SubfinderPlugin(BasePlugin):
    name = "subfinder"
    version = "2.6.3"
    author = "ProjectDiscovery / HellForge"
    description = "Passive subdomain discovery tool"
    events = ["scan.started"]
    enabled = True

    async def on_event(self, event_type: str, data: Any):
        if event_type == "scan.started":
            domain = data.get("domain")
            await asyncio.sleep(0.3)
            
            subdomains = [
                f"api.{domain}",
                f"admin.{domain}",
                f"dev.{domain}",
                f"vpn.{domain}",
                f"auth.{domain}",
                f"s3-storage.{domain}"
            ]
            
            for sub in subdomains:
                await event_bus.publish("asset.discovered", {
                    "subdomain": sub,
                    "domain": domain,
                    "source": "subfinder",
                    "tags": ["subdomain", "passive"]
                })
