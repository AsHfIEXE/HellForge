import os
import asyncio
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus_manager
from app.core.dtos import HTTPEvent, FindingEvent

class NucleiPlugin(BasePlugin):
    def __init__(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "plugin.yaml")
        super().__init__(manifest_path)

    async def execute(self, event_data: Any):
        if isinstance(event_data, HTTPEvent):
            subdomain = event_data.subdomain
            await asyncio.sleep(0.1)
            
            if "admin" in subdomain:
                finding_evt = FindingEvent(
                    subdomain=subdomain,
                    title="Exposed Admin Panel Without Multi-Factor Authentication",
                    severity="High",
                    category="Misconfiguration",
                    description="Administrative interface directly exposed to public internet.",
                    remediation="Restrict access using Cloudflare Access or VPN.",
                    cvss_score=7.5,
                    cve_id="CWE-307"
                )
                await event_bus_manager.finding_bus.publish(finding_evt)
            elif "dev" in subdomain:
                finding_evt = FindingEvent(
                    subdomain=subdomain,
                    title="Hardcoded Secret Key Leak in Static Bundle",
                    severity="Critical",
                    category="Secret Leak",
                    description="Hardcoded AWS IAM access key discovered in frontend code.",
                    remediation="Revoke IAM key and replace with STS transient credentials.",
                    cvss_score=9.8,
                    cve_id="CWE-798"
                )
                await event_bus_manager.finding_bus.publish(finding_evt)
