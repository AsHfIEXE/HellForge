import pytest
from app.core.risk_engine import ModularRiskEngine
from app.core.dtos import FindingEvent

def test_risk_engine_base_calculation():
    engine = ModularRiskEngine()
    result = engine.calculate_asset_risk(
        base_score=10.0,
        is_internet_facing=True,
        auth_required=False
    )
    assert result["risk_score"] == 25.0
    assert result["rating"] == "Low"

def test_risk_engine_critical_cve():
    engine = ModularRiskEngine()
    finding = FindingEvent(
        subdomain="dev.example.com",
        title="Critical RCE",
        severity="Critical",
        category="RCE",
        description="Remote code execution vulnerability"
    )
    result = engine.calculate_asset_risk(
        base_score=20.0,
        is_internet_facing=True,
        findings=[finding],
        auth_required=False
    )
    # 20.0 (base) + 15.0 (exposure) + 35.0 (Critical CVE) = 70.0 (High)
    assert result["risk_score"] == 70.0
    assert result["rating"] == "High"
