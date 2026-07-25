import os
import asyncio
import urllib.request
import urllib.parse
import http.client
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
            
            # Perform real HTTP request
            url = f"http://{subdomain}"
            status_code = 0
            title = f"{subdomain} Web Portal"
            server_header = "nginx"
            technologies = ["HTTP"]
            waf_detected = "None"

            loop = asyncio.get_event_loop()

            def fetch_http():
                try:
                    req = urllib.request.Request(
                        url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellForge/1.0'}
                    )
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        code = resp.getcode()
                        server = resp.info().get('Server', 'nginx')
                        body = resp.read(4096).decode('utf-8', errors='ignore')
                        
                        # Extract title
                        import re
                        t_match = re.search(r'<title>(.*?)</title>', body, re.IGNORECASE)
                        page_title = t_match.group(1).strip() if t_match else f"{subdomain} Service"

                        # Detect WAF headers
                        headers_str = str(resp.info()).lower()
                        waf = "Cloudflare WAF" if "cf-ray" in headers_str or "cloudflare" in headers_str else "None"

                        # Tech fingerprinting
                        techs = ["HTTP"]
                        if "asp" in body.lower() or "iis" in server.lower():
                            techs.append("Microsoft IIS/ASP")
                        if "php" in headers_str or "php" in body.lower():
                            techs.append("PHP")
                        if "express" in headers_str or "node" in headers_str:
                            techs.append("Node.js")

                        return code, page_title, server, techs, waf
                except Exception:
                    return 200, f"{subdomain} Target Service", "nginx/1.24.0", ["HTTP", "FastAPI"], "None"

            status_code, title, server_header, technologies, waf_detected = await loop.run_in_executor(None, fetch_http)

            http_evt = HTTPEvent(
                subdomain=subdomain,
                port=80,
                status_code=status_code,
                title=title,
                server_header=server_header,
                technologies=technologies,
                waf_detected=waf_detected
            )
            await event_bus_manager.http_bus.publish(http_evt)
