import os
import asyncio
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus_manager
from app.core.dtos import AssetEvent, HTTPEvent

class HTTPXPlugin(BasePlugin):
    def __init__(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "plugin.yaml")
        super().__init__(manifest_path)

    async def execute(self, event_data: Any):
        if isinstance(event_data, AssetEvent):
            subdomain = event_data.subdomain
            await asyncio.sleep(0.1)
            
            http_evt = HTTPEvent(
                subdomain=subdomain,
                port=443,
                status_code=200 if "api" in subdomain else 401 if "admin" in subdomain else 200,
                title=f"{subdomain} Gateway",
                server_header="nginx/1.24.0",
                technologies=["FastAPI", "React", "Cloudflare WAF"],
                waf_detected="Cloudflare WAF" if "admin" in subdomain else "None"
            )
            # Publish to http_bus topic channel
            await event_bus_manager.http_bus.publish(http_evt)
