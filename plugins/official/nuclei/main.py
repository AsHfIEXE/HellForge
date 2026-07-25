import os
import asyncio
import urllib.request
import re
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

            loop = asyncio.get_event_loop()

            def analyze_vulnerabilities():
                url = f"http://{subdomain}"
                findings = []
                try:
                    req = urllib.request.Request(
                        url,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellForge/1.0'}
                    )
                    with urllib.request.urlopen(req, timeout=3) as resp:
                        headers = str(resp.info()).lower()
                        body = resp.read(8192).decode('utf-8', errors='ignore').lower()

                        # 1. Missing Security Headers
                        if "x-frame-options" not in headers:
                            findings.append({
                                "title": "Missing X-Frame-Options Security Header",
                                "severity": "Low",
                                "category": "Clickjacking",
                                "description": f"Target host {subdomain} lacks clickjacking defense headers.",
                                "remediation": "Add X-Frame-Options: DENY or SAMEORIGIN.",
                                "cvss": 4.3,
                                "cve": "CWE-1021"
                            })

                        if "content-security-policy" not in headers:
                            findings.append({
                                "title": "Missing Content-Security-Policy (CSP) Header",
                                "severity": "Medium",
                                "category": "CSP",
                                "description": f"No CSP policy header detected on {subdomain}.",
                                "remediation": "Implement strict Content-Security-Policy header.",
                                "cvss": 5.4,
                                "cve": "CWE-693"
                            })

                        # 2. Outdated Server / ASP / IIS signatures
                        if "asp.net" in headers or "iis" in headers or "asp" in body:
                            findings.append({
                                "title": "Exposed Legacy ASP / IIS Technology Stack",
                                "severity": "Medium",
                                "category": "Information Disclosure",
                                "description": f"Exposed legacy ASP framework headers detected on {subdomain}.",
                                "remediation": "Suppress Server and X-Powered-By response headers.",
                                "cvss": 5.0,
                                "cve": "CWE-200"
                            })

                except Exception:
                    pass

                return findings

            discovered_findings = await loop.run_in_executor(None, analyze_vulnerabilities)

            for f in discovered_findings:
                finding_evt = FindingEvent(
                    subdomain=subdomain,
                    title=f["title"],
                    severity=f["severity"],
                    category=f["category"],
                    description=f["description"],
                    remediation=f["remediation"],
                    cvss_score=f["cvss"],
                    cve_id=f["cve"],
                    discovery_source="nuclei"
                )
                await event_bus_manager.finding_bus.publish(finding_evt)
