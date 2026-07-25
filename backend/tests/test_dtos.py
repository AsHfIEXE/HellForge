import pytest
from app.core.dtos import ScanContext, AssetEvent, HTTPEvent, FindingEvent, RiskEvent

def test_scan_context_creation():
    ctx = ScanContext(target_domain="example.com")
    assert ctx.target_domain == "example.com"
    assert ctx.scan_id is not None
    assert ctx.started_by == "system"

def test_asset_event_dto():
    asset = AssetEvent(
        scan_id="test-scan-123",
        domain="example.com",
        subdomain="api.example.com",
        tags=["api", "passive"],
        discovery_source="subfinder"
    )
    assert asset.subdomain == "api.example.com"
    assert asset.discovery_source == "subfinder"
    assert "api" in asset.tags

def test_finding_event_dto():
    finding = FindingEvent(
        subdomain="admin.example.com",
        title="Exposed Admin Portal",
        severity="High",
        category="Misconfiguration",
        description="Publicly exposed portal",
        remediation="Restrict access via WAF"
    )
    assert finding.severity == "High"
    assert finding.cvss_score == 0.0
