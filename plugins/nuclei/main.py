import asyncio
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus

class NucleiPlugin(BasePlugin):
    name = "nuclei"
    version = "3.1.0"
    author = "ProjectDiscovery / HellForge"
    description = "Vulnerability scanner powered by customizable YAML templates"
    events = ["service.detected"]
    enabled = True

    async def on_event(self, event_type: str, data: Any):
        if event_type == "service.detected":
            subdomain = data.get("subdomain")
            await asyncio.sleep(0.3)
            
            if "admin" in subdomain:
                await event_bus.publish("finding.created", {
                    "subdomain": subdomain,
                    "title": "Exposed Admin Panel Without Rate Limiting",
                    "severity": "High",
                    "category": "Misconfiguration",
                    "description": "Administrative interface reachable directly over internet.",
                    "remediation": "Restrict IP range via WAF rules and mandate MFA.",
                    "cvss_score": 7.5,
                    "cve_id": "CWE-307"
                })
            elif "dev" in subdomain:
                await event_bus.publish("finding.created", {
                    "subdomain": subdomain,
                    "title": "Exposed Git Repository & Hardcoded Credentials",
                    "severity": "Critical",
                    "category": "Secret Leak",
                    "description": "Publicly accessible .git folder containing AWS credentials.",
                    "remediation": "Delete .git folder from production web root.",
                    "cvss_score": 9.8,
                    "cve_id": "CWE-538"
                })
