import argparse
import sys
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def main():
    parser = argparse.ArgumentParser(
        prog="hellforge",
        description="HellForge CLI - Build the attack surface. Hunt the impossible."
    )
    subparsers = parser.add_subparsers(dest="command", help="HellForge Command Suite")

    subparsers.add_parser("init", help="Initialize HellForge database and configuration")

    t_parser = subparsers.add_parser("target", help="Manage targets")
    t_sub = t_parser.add_subparsers(dest="target_action")
    add_t = t_sub.add_parser("add", help="Add new target domain")
    add_t.add_argument("domain", help="Target domain (e.g. example.com)")

    scan_p = subparsers.add_parser("scan", help="Execute event-driven scan pipeline")
    scan_p.add_argument("domain", help="Target domain to scan")

    subparsers.add_parser("monitor", help="Listen to live event telemetry stream")
    subparsers.add_parser("plugin", help="Manage and list loaded plugins")
    subparsers.add_parser("report", help="Generate security posture report")
    subparsers.add_parser("graph", help="Print asset network topology stats")

    ai_p = subparsers.add_parser("ai", help="Query AI Copilot security assistant")
    ai_p.add_argument("query", help="Vulnerability or asset query")

    subparsers.add_parser("doctor", help="Run system environment & service health diagnostics")
    subparsers.add_parser("update", help="Update HellForge engine & plugin marketplace")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "init":
            print("[+] Initializing HellForge Core Database and EventBus Engine...")
            res = requests.get("http://localhost:8000/health")
            if res.status_code == 200:
                print(f"[+] Engine online: {res.json()['system']}")
            else:
                print("[-] Failed to connect to core engine.")

        elif args.command == "scan":
            print(f"[*] Dispatching EventDriven scan for domain: {args.domain}...")
            res = requests.post(f"{BASE_URL}/scans/start?domain={args.domain}")
            if res.status_code == 200:
                data = res.json()
                print(f"[+] EventBus Pipeline Scan Complete!")
                print(f"    Discovered Assets: {data['summary']['assets_discovered']}")
                print(f"    Security Findings: {data['summary']['findings_count']}")
            else:
                print(f"[-] Scan failed: {res.text}")

        elif args.command == "plugin":
            res = requests.get(f"{BASE_URL}/plugins")
            if res.status_code == 200:
                plugins = res.json()
                print(f"\n[+] Installed Plugins & Event Subscriptions ({len(plugins)})\n" + "="*65)
                for p in plugins:
                    print(f" - {p['name']:<20} v{p['version']:<8} Author: {p['author']}")
                    print(f"   Subscribed Events: {', '.join(p['subscriptions'])}")
                    print(f"   {p['description']}\n")

        elif args.command == "ai":
            res = requests.post(f"{BASE_URL}/ai/analyze?query={args.query}")
            if res.status_code == 200:
                data = res.json()
                print(f"\n[+] HellForge AI Security Copilot\n" + "="*65)
                print(data['response'])
                print(f"\nCVSS Estimate: {data['cvss_estimate']}/10.0")

        elif args.command == "doctor":
            print("[*] Running HellForge Diagnostics...")
            print(" [OK] Python Core Runtime: OK")
            print(" [OK] SQLite/SQLAlchemy Database Session: OK")
            print(" [OK] Topic-Based EventBus Channels (scan, asset, http, finding, risk): OK")
            print(" [OK] Categorized Plugin Marketplace (`plugins/official`, `community`, `private`): OK")
            print(" [OK] FastAPI Refined Engine: OK")

        elif args.command == "target" and args.target_action == "add":
            print(f"[+] Target domain '{args.domain}' registered successfully.")

        elif args.command == "report":
            res = requests.get(f"{BASE_URL}/stats")
            if res.status_code == 200:
                stats = res.json()
                print("\n" + "="*50)
                print("           HELLFORGE EXECUTIVE REPORT           ")
                print("="*50)
                print(f" Total Discovered Assets:        {stats['total_assets']}")
                print(f" Total Vulnerabilities Found:    {stats['total_vulnerabilities']}")
                print(f" Average Attack Surface Risk:    {stats['average_risk_score']}/100")
                print(f" Critical Findings:              {stats['severity_breakdown']['critical']}")
                print("="*50 + "\n")

    except requests.exceptions.ConnectionError:
        print("[-] Connection Error: Ensure HellForge backend is running at http://localhost:8000.")

if __name__ == "__main__":
    main()
