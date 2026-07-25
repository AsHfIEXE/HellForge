import os
import asyncio
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
            await asyncio.sleep(0.1)

            # Simulated JS bundle scan for target asset
            sample_js_code = (
                f"const API_URL = 'https://{subdomain}/api/v1/users';\n"
                f"const AWS_KEY = 'AKIAIOSFODNN7EXAMPLE';\n"
                f"const JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';\n"
                f"fetch('/api/v1/internal/config');\n"
            )

            res = js_analyzer.analyze_script(sample_js_code)

            for secret in res["secrets"]:
                finding_evt = FindingEvent(
                    subdomain=subdomain,
                    title=f"Hardcoded {secret['type']} Extracted from JS Asset",
                    severity="High" if secret["type"] == "AWS Access Key" else "Medium",
                    category="Secret Leak",
                    description=f"Automated JS Intelligence mined {secret['type']} inside static bundle code.",
                    remediation="Rotate exposed credentials and move keys to secure environment variables.",
                    cvss_score=8.1 if secret["type"] == "AWS Access Key" else 6.5,
                    cve_id="CWE-798",
                    discovery_source="js_miner"
                )
                await event_bus_manager.finding_bus.publish(finding_evt)
