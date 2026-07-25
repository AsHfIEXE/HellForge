import datetime
from typing import Dict, Any, List

class ExecutiveReporter:
    """
    Generates standalone styled HTML and Markdown executive security posture reports.
    """
    @staticmethod
    def generate_markdown_report(
        target_domain: str,
        stats: Dict[str, Any],
        assets: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> str:
        
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        md = []
        md.append(f"# HellForge Executive Security Report: {target_domain}")
        md.append(f"**Generated:** {timestamp}\n")
        md.append("## Executive Summary")
        md.append(f"- **Total Discovered Assets:** {stats.get('total_assets', len(assets))}")
        md.append(f"- **Total Security Findings:** {stats.get('total_vulnerabilities', len(findings))}")
        md.append(f"- **Average Risk Score:** {stats.get('average_risk_score', 0.0)} / 100")
        md.append(f"- **Critical Severity Findings:** {stats.get('severity_breakdown', {}).get('critical', 0)}\n")

        md.append("## Discovered Attack Surface Inventory")
        for a in assets:
            md.append(f"- **{a.get('name')}** | Risk Score: `{a.get('risk_score')}/100` | Source: `{a.get('discovery_source')}`")

        md.append("\n## Critical Vulnerabilities & Remediation Roadmap")
        for f in findings:
            md.append(f"### [{f.get('severity', 'INFO')}] {f.get('title')}")
            md.append(f"**Category:** {f.get('category')} | **CVSS:** {f.get('cvss_score', 0.0)}")
            md.append(f"**Description:** {f.get('description')}")
            md.append(f"**Remediation:** {f.get('remediation')}\n")

        return "\n".join(md)

    @staticmethod
    def generate_html_report(
        target_domain: str,
        stats: Dict[str, Any],
        assets: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> str:
        
        md_content = ExecutiveReporter.generate_markdown_report(target_domain, stats, assets, findings)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>HellForge Security Report - {target_domain}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #090c10; color: #f0f6fc; padding: 40px; line-height: 1.6; }}
        h1 {{ color: #ff3b5c; border-bottom: 2px solid #30363d; padding-bottom: 10px; }}
        h2 {{ color: #00f0ff; margin-top: 30px; }}
        .card {{ background: rgba(18, 22, 31, 0.85); border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 16px; }}
        .badge-crit {{ background: rgba(255, 59, 92, 0.2); color: #ff3b5c; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        code {{ background: #161b22; padding: 2px 6px; border-radius: 4px; color: #79c0ff; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>HELLFORGE EXECUTIVE POSTURE REPORT</h1>
        <p><strong>Target Scope:</strong> {target_domain}</p>
        <p><strong>Generated At:</strong> {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}</p>
    </div>
    <div class="card">
        <h2>Risk & Exposure Metrics</h2>
        <p>Total Assets Mapped: <strong>{len(assets)}</strong></p>
        <p>Total Security Vulnerabilities: <strong>{len(findings)}</strong></p>
    </div>
</body>
</html>"""
        return html

executive_reporter = ExecutiveReporter()
