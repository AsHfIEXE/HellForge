import pytest
import pytest_asyncio
from app.engine.js_intel import js_analyzer
from app.engine.reporter import executive_reporter
from app.engine.scheduler import delta_tracker

def test_js_intel_analyzer_secret_extraction():
    js_code = """
    const API_KEY = "AKIA1234567890ABCDEF";
    const bearer = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature";
    fetch("/api/v1/internal/config");
    """
    results = js_analyzer.analyze_script(js_code)
    assert results["total_secrets"] >= 1
    assert "/api/v1/internal/config" in results["endpoints"]

def test_change_delta_tracker():
    prev_assets = [{"name": "api.example.com"}, {"name": "admin.example.com"}]
    curr_assets = [{"name": "api.example.com"}, {"name": "admin.example.com"}, {"name": "dev.example.com"}]
    
    delta = delta_tracker.calculate_delta(prev_assets, curr_assets, [], [])
    assert delta["new_assets_count"] == 1
    assert "dev.example.com" in delta["new_assets"]

def test_executive_reporter_markdown_generation():
    stats = {"total_assets": 2, "total_vulnerabilities": 1, "average_risk_score": 50.0}
    assets = [{"name": "api.example.com", "risk_score": 40, "discovery_source": "subfinder"}]
    findings = [{"title": "Exposed Key", "severity": "High", "category": "Secret Leak", "description": "Key leak", "remediation": "Rotate key"}]

    md = executive_reporter.generate_markdown_report("example.com", stats, assets, findings)
    assert "# HellForge Executive Security Report" in md
    assert "api.example.com" in md
    assert "Exposed Key" in md

def test_executive_reporter_html_generation():
    stats = {"total_assets": 2, "total_vulnerabilities": 1, "average_risk_score": 50.0}
    assets = [{"name": "api.example.com", "risk_score": 40, "discovery_source": "subfinder"}]
    findings = [{"title": "Exposed Key", "severity": "High", "category": "Secret Leak", "description": "Key leak", "remediation": "Rotate key"}]

    html = executive_reporter.generate_html_report("example.com", stats, assets, findings)
    assert "<!DOCTYPE html>" in html
    assert "HELLFORGE EXECUTIVE POSTURE REPORT" in html
