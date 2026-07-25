import requests
import json
import sys
import time

BASE = "http://localhost:8000"
API  = f"{BASE}/api/v1"
errors = []
passed = 0

def check(label, fn):
    global passed
    try:
        fn()
        print(f"  [PASS] {label}")
        passed += 1
    except Exception as e:
        errors.append(label)
        print(f"  [FAIL] {label}: {e}")

print("=" * 60)
print("  HELLFORGE END-TO-END INTEGRATION TESTS")
print("=" * 60)

# Wait for server
for i in range(5):
    try:
        requests.get(f"{BASE}/health", timeout=2)
        break
    except:
        time.sleep(1)

# 1. Health Check
def test_health():
    r = requests.get(f"{BASE}/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "online"
    assert "topic_channels" in data

check("Health Check Endpoint", test_health)

# 2. Execute Scan Pipeline
def test_scan():
    r = requests.post(f"{API}/scans/start?domain=hellforge-test.io")
    assert r.status_code == 200
    data = r.json()
    assert data["summary"]["assets_discovered"] > 0
    assert data["summary"]["findings_count"] > 0

check("Scan Pipeline Execution (hellforge-test.io)", test_scan)

# 3. Assets API
def test_assets():
    r = requests.get(f"{API}/assets")
    assert r.status_code == 200
    assets = r.json()
    assert len(assets) > 0
    assert "name" in assets[0]
    assert "risk_score" in assets[0]

check("Assets API Response", test_assets)

# 4. Findings API
def test_findings():
    r = requests.get(f"{API}/findings")
    assert r.status_code == 200
    findings = r.json()
    assert len(findings) > 0

check("Findings API Response", test_findings)

# 5. Graph API
def test_graph():
    r = requests.get(f"{API}/graph")
    assert r.status_code == 200
    data = r.json()
    assert "nodes" in data
    assert "links" in data
    assert len(data["nodes"]) > 1

check("Attack Graph API Response", test_graph)

# 6. Plugins API
def test_plugins():
    r = requests.get(f"{API}/plugins")
    assert r.status_code == 200
    plugins = r.json()
    assert len(plugins) >= 3
    names = [p["name"] for p in plugins]
    assert "subfinder" in names
    assert "httpx" in names
    assert "nuclei" in names

check("Plugin Marketplace API (3 official plugins)", test_plugins)

# 7. Timeline API
def test_timeline():
    r = requests.get(f"{API}/timeline")
    assert r.status_code == 200
    events = r.json()
    assert len(events) > 0

check("Timeline Events API", test_timeline)

# 8. Stats/Dashboard API
def test_stats():
    r = requests.get(f"{API}/stats")
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_assets"] > 0
    assert "severity_breakdown" in stats

check("Dashboard Stats API", test_stats)

# 9. AI Copilot API
def test_ai():
    r = requests.post(f"{API}/ai/analyze?query=XSS-on-admin-panel")
    assert r.status_code == 200
    data = r.json()
    assert "response" in data
    assert "cvss_estimate" in data

check("AI Copilot Analyze API", test_ai)

# 10. CLI Doctor (offline, no server needed)
import subprocess
def test_cli():
    result = subprocess.run(
        [sys.executable, "cli/hellforge_cli.py", "doctor"],
        capture_output=True, text=True, cwd="c:\\Users\\user\\Desktop\\HellForge"
    )
    assert result.returncode == 0
    assert "[OK]" in result.stdout

check("CLI Doctor Command", test_cli)

print("=" * 60)
print(f"  RESULTS: {passed} passed, {len(errors)} failed")
if errors:
    print(f"  FAILURES: {', '.join(errors)}")
else:
    print("  ALL TESTS PASSED - HELLFORGE PHASE 1 VERIFIED")
print("=" * 60)

sys.exit(1 if errors else 0)
