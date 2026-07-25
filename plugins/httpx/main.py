import asyncio
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus

class HTTPXPlugin(BasePlugin):
    name = "httpx"
    version = "1.3.5"
    author = "ProjectDiscovery / HellForge"
    description = "Fast and multi-purpose HTTP toolkit"
    events = ["asset.discovered"]
    enabled = True

    async def on_event(self, event_type: str, data: Any):
        if event_type == "asset.discovered":
            subdomain = data.get("subdomain")
            await asyncio.sleep(0.2)
            
            # Emit HTTP response telemetry event
            http_data = {
                "subdomain": subdomain,
                "port": 443,
                "status_code": 200 if "api" in subdomain else 401 if "admin" in subdomain else 200,
                "title": f"{subdomain} - Gateway Portal",
                "server": "nginx/1.24.0",
                "technologies": ["React", "FastAPI", "Cloudflare WAF"],
                "waf": "Cloudflare WAF" if "admin" in subdomain or "auth" in subdomain else "None"
            }
            
            await event_bus.publish("http.response", http_data)
            await event_bus.publish("service.detected", {
                "subdomain": subdomain,
                "port": 443,
                "service": "https",
                "http_data": http_data
            })
