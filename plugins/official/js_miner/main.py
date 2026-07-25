import os
import asyncio
import urllib.request
import re
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus_manager
from app.core.dtos import HTTPEvent, FindingEvent
from app.engine.js_intel import js_analyzer

class JSMinerPlugin(BasePlugin):
    def __init__(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "plugin.yaml")
        super().__init__(manifest_path)

    async def execute(self, event_data: Any):
        if isinstance(event_data, HTTPEvent):
            subdomain = event_data.subdomain

            loop = asyncio.get_event_loop()

            def fetch_and_mine():
                url = f"http://{subdomain}"
                try:
                    req = urllib.request.Request(
                        url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellForge/1.0'}
                    )
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        body = resp.read(8192).decode('utf-8', errors='ignore')
                        return js_analyzer.analyze_script(body)
                except Exception:
                    return {"secrets": [], "endpoints": []}

            res = await loop.run_in_executor(None, fetch_and_mine)

            for secret in res.get("secrets", []):
                finding_evt = FindingEvent(
                    subdomain=subdomain,
                    title=f"Discovered {secret['type']} in Web Asset",
                    severity="High" if secret["type"] in ["AWS Access Key", "JWT Token"] else "Medium",
                    category="Secret Leak",
                    description=f"Real-time JS Intelligence mined {secret['type']} on target {subdomain}.",
                    remediation="Rotate exposed keys immediately and secure endpoint configuration.",
                    cvss_score=8.1 if secret["type"] == "AWS Access Key" else 6.5,
                    cve_id="CWE-798",
                    discovery_source="js_miner"
                )
                await event_bus_manager.finding_bus.publish(finding_evt)
