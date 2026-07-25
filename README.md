<div align="center">

# HELLFORGE
### *Build the attack surface. Hunt the impossible.*

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18-61DAFB.svg)](https://reactjs.org)
[![Event Driven](https://img.shields.io/badge/Architecture-Event--Driven-purple.svg)](#system-architecture)

**HellForge** is a modular, event-driven Attack Surface Management (ASM) and Security Intelligence Platform. It unifies passive reconnaissance, HTTP intelligence, JavaScript secret extraction, vulnerability correlation, multi-factor risk scoring, and AI-assisted threat vector analysis into a single ecosystem.

</div>

---

## System Architecture

```text
                           Web Dashboard (React + Vite + Cyber UI)
                                             │
      ┌──────────────────────────────────────┼──────────────────────────────────────┐
      ▼                                      ▼                                      ▼
 REST API (v1)                       WebSocket Telemetry                        CLI Utility
      │                                      │                                      │
      └──────────────────────────────────────┼──────────────────────────────────────┘
                                             ▼
                             Topic-Based Event Bus Manager
                                             │
      ┌───────────────┬───────────────┬──────┴────────┬───────────────┬───────────────┐
      ▼               ▼               ▼               ▼               ▼               ▼
  scan_bus        asset_bus       http_bus       finding_bus      risk_bus       system_bus
 (ScanContext)   (AssetEvent)    (HTTPEvent)    (FindingEvent)   (RiskEvent)
      │               │               │               │               │               │
      └───────────────┴───────────────┼───────────────┴───────────────┴───────────────┘
                                      ▼
                        Categorized Plugin Marketplace
                     ┌────────────────────────────────┐
                     │  plugins/official/             │
                     │    ├── subfinder               │
                     │    ├── httpx                   │
                     │    └── nuclei                  │
                     │  plugins/community/            │
                     │  plugins/private/              │
                     └────────────────────────────────┘
                                      │
                                      ▼
                        Multi-Factor Risk Scoring Engine
                                      │
                                      ▼
                      SQLAlchemy Async Relational Database
```

---

## Key Features

- **Event-Driven Topic Engine:** Decoupled Pub/Sub messaging prevents event flooding across unrelated plugins (`scan`, `asset`, `http`, `finding`, `risk`, `system`).
- **Immutable DTO Contracts:** Strict Pydantic models (`ScanContext`, `AssetEvent`, `HTTPEvent`, `FindingEvent`, `RiskEvent`) ensure plugins communicate cleanly without mutating ORM state directly.
- **Modular Multi-Factor Risk Engine:** Dynamically calculates 0–100 asset risk scores using independent scorers (`ExposureScorer`, `CVEScorer`, `TechnologyScorer`, `AuthScorer`).
- **Categorized Plugin Marketplace:** Auto-discovers plugins from `plugins/official`, `plugins/community`, and `plugins/private` with `plugin.yaml` manifest validation.
- **HellForge CLI Utility:** Full command-line suite (`hellforge doctor`, `hellforge scan`, `hellforge plugin`, `hellforge report`, `hellforge ai`).
- **Cyber Glassmorphism Dashboard:** Interactive React dashboard featuring D3.js Network Topology graphs and live AI Security Copilot.

---

## Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m pytest tests  # Run automated test suite
python app/main.py      # Launch FastAPI server
```

### 3. Frontend Dashboard Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Docker Deployment
```bash
docker-compose up --build
```

---

## CLI Usage

The `hellforge` CLI allows security engineers to execute scans, inspect plugin marketplaces, and run system health checks directly from the terminal.

```bash
# Run system diagnostics
python cli/hellforge_cli.py doctor

# Add a target domain
python cli/hellforge_cli.py target add example.com

# Execute Event-Driven Scan Pipeline
python cli/hellforge_cli.py scan example.com

# List installed marketplace plugins and event subscriptions
python cli/hellforge_cli.py plugin

# Generate Executive Security Posture Report
python cli/hellforge_cli.py report

# Query HellForge AI Copilot
python cli/hellforge_cli.py ai "Explain XSS vector on dev portal"
```

---

## Writing a Third-Party Plugin

Plugins are self-contained modules located under `plugins/community/<plugin_name>/`.

### Step 1: Create `plugin.yaml`
```yaml
name: custom_subdomain_hunter
version: 1.0.0
author: Security Researcher
description: Custom passive subdomain collector plugin
subscriptions:
  - scan
```

### Step 2: Create `main.py`
```python
import os
import asyncio
from typing import Any
from app.plugins.sdk import BasePlugin
from app.core.events import event_bus_manager
from app.core.dtos import ScanContext, AssetEvent

class CustomSubdomainHunter(BasePlugin):
    def __init__(self):
        manifest_path = os.path.join(os.path.dirname(__file__), "plugin.yaml")
        super().__init__(manifest_path)

    async def execute(self, event_data: Any):
        if isinstance(event_data, ScanContext):
            domain = event_data.target_domain
            
            # Emit discovered asset DTO to asset_bus
            asset_evt = AssetEvent(
                scan_id=event_data.scan_id,
                domain=domain,
                subdomain=f"internal-auth.{domain}",
                tags=["custom", "passive"],
                discovery_source="custom_hunter"
            )
            await event_bus_manager.asset_bus.publish(asset_evt)
```

---

## Project Roadmap & Implementation Plan

```text
[Phase 1] ──► [Phase 2] ──► [Phase 3] ──► [Phase 4] ──► [Phase 5]
 Core Platform   Recon & JS    Distributed    Enterprise    Continuous
 Engine          Intel         Workers & AI   RBAC          ASM
```

### Phase 1: Core Framework (Completed)
- [x] Topic-based split event bus engine
- [x] Immutable Pydantic DTO data contracts
- [x] Plugin SDK with `plugin.yaml` manifest validation
- [x] Categorized plugin marketplace loader (`official`, `community`, `private`)
- [x] Modular multi-factor risk engine
- [x] FastAPI REST API (v1) & WebSocket telemetry channel
- [x] Rich terminal CLI tool (`hellforge doctor`, `scan`, `report`, `plugin`, `ai`)
- [x] Cyberpunk React dashboard with D3 topology graph
- [x] Docker Compose deployment configuration
- [x] Automated test suite (Pytest integration)

### Phase 2: Advanced Reconnaissance & JS Intelligence (Completed)
- [x] Automated JavaScript bundle downloading and AST parsing for secret detection
- [x] Scheduled & recurring target scanning engine with change delta tracking
- [x] Executive report generation engine (HTML & Markdown format)
- [x] Screenshot visual interface classifier engine


### Phase 3: Distributed Workers & Cloud Connectors
- [ ] Redis / NATS Message Queue backend plugin for EventBus scaling
- [ ] Remote agent worker nodes for distributed scanning across VPCs
- [ ] AWS, Azure, GCP, and Cloudflare asset discovery connectors
- [ ] Local RAG AI engine over scan results using Ollama & vector databases

### Phase 4: Enterprise RBAC & Multi-Tenancy
- [ ] Role-Based Access Control (Admin, Analyst, Auditor, Viewer)
- [ ] Project-scoped user permissions & JWT refresh token authentication
- [ ] Third-party integrations (Slack alerts, Jira issue creation, GitHub actions, SIEM webhooks)
- [ ] Web-based Plugin Marketplace store UI

### Phase 5: Continuous Attack Surface Management (EASM)
- [ ] Historical asset evolution & change-delta tracking (Assets added/removed over time)
- [ ] Exposure trend analytics & CVSS threat heatmaps
- [ ] Automated remediation verification & SLA tracking
- [ ] High-availability Kubernetes deployment manifests (Helm chart)

---

## License

Distributed under the MIT License. See `LICENSE` for details.
