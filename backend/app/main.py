from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
import asyncio
import json

from app.core.config import settings
from app.db.database import get_db, init_db
from app.db.models import (
    Organization, Project, Target, Domain, Subdomain, Service, Finding, Scan, TimelineEvent
)
from app.engine.orchestrator import event_orchestrator
from app.plugins.loader import plugin_loader
from app.core.events import event_bus_manager
from app.core.risk_engine import risk_engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

ws_manager = ConnectionManager()

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "system": "HellForge Refined Architecture v1.0",
        "topic_channels": list(event_bus_manager.channels.keys()),
        "plugins": len(plugin_loader.loaded_plugins)
    }

# --- WebSocket Telemetry Channel ---
@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# --- Dashboard & Stats API ---
@app.get("/api/v1/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    subs_res = await db.execute(select(Subdomain))
    subs = subs_res.scalars().all()

    findings_res = await db.execute(select(Finding))
    findings = findings_res.scalars().all()

    projects_res = await db.execute(select(Project))
    projects = projects_res.scalars().all()

    targets_res = await db.execute(select(Target))
    targets = targets_res.scalars().all()

    critical_count = sum(1 for f in findings if f.severity == "Critical")
    high_count = sum(1 for f in findings if f.severity == "High")
    med_count = sum(1 for f in findings if f.severity == "Medium")
    low_count = sum(1 for f in findings if f.severity == "Low")

    avg_risk = float(sum(s.risk_score for s in subs) / len(subs)) if subs else 0.0

    return {
        "total_projects": len(projects),
        "total_targets": len(targets),
        "total_assets": len(subs),
        "total_vulnerabilities": len(findings),
        "average_risk_score": round(avg_risk, 1),
        "severity_breakdown": {
            "critical": critical_count,
            "high": high_count,
            "medium": med_count,
            "low": low_count
        }
    }

# --- Scan Engine API ---
@app.post("/api/v1/scans/start")
async def start_scan(domain: str, db: AsyncSession = Depends(get_db)):
    scan = await event_orchestrator.run_pipeline(db, domain)
    return {"message": "Scan completed via Topic EventBus pipeline", "scan_id": scan.id, "summary": scan.summary}

@app.get("/api/v1/scans")
async def get_scans(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Scan).order_by(Scan.started_at.desc()))
    return res.scalars().all()

# --- Assets API ---
@app.get("/api/v1/assets")
async def get_assets(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Subdomain))
    subs = res.scalars().all()
    
    output = []
    for s in subs:
        output.append({
            "id": s.id,
            "name": s.name,
            "risk_score": s.risk_score,
            "tags": s.tags,
            "discovery_source": s.discovery_source,
            "first_seen": s.first_seen.isoformat(),
            "last_seen": s.last_seen.isoformat()
        })
    return output

@app.get("/api/v1/assets/{asset_id}/risk")
async def get_asset_risk(asset_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Subdomain).where(Subdomain.id == asset_id)
    res = await db.execute(stmt)
    sub = res.scalars().first()
    if not sub:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    is_admin = "admin" in sub.name or "dev" in sub.name
    return risk_engine.calculate_asset_risk(
        base_score=15.0,
        is_internet_facing=True,
        auth_required=not is_admin
    )

# --- Graph API ---
@app.get("/api/v1/graph")
async def get_attack_graph(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Subdomain))
    subs = res.scalars().all()

    nodes = [{"id": "HellForge Security Mesh", "group": "root", "risk": 0}]
    links = []

    for s in subs:
        nodes.append({
            "id": s.name,
            "group": "subdomain",
            "risk": s.risk_score,
            "tags": s.tags
        })
        links.append({
            "source": "HellForge Security Mesh",
            "target": s.name
        })

    return {"nodes": nodes, "links": links}

# --- Findings API ---
@app.get("/api/v1/findings")
async def get_findings(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Finding))
    return res.scalars().all()

# --- Plugins API ---
@app.get("/api/v1/plugins")
def get_plugins():
    return plugin_loader.list_plugins()

# --- Timeline API ---
@app.get("/api/v1/timeline")
async def get_timeline(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(TimelineEvent).order_by(TimelineEvent.created_at.desc()))
    return res.scalars().all()

# --- AI Copilot API ---
@app.post("/api/v1/ai/analyze")
def ai_copilot_analysis(query: str):
    return {
        "query": query,
        "response": (
            f"### HellForge AI Threat Vector Analysis\n\n"
            f"**Observed Attack Vector (`{query}`):**\n"
            f"1. **Reconnaissance:** Asset discovered via passive subdomain intelligence.\n"
            f"2. **Risk Impact:** Unrestricted access combined with lack of MFA token verification presents potential SSRF / credential leak vector.\n\n"
            f"**Remediation Guidance:**\n"
            f"- Restrict internal interfaces with Cloudflare Access or mTLS.\n"
            f"- Rotate exposed keys immediately."
        ),
        "cvss_estimate": 8.5,
        "references": ["https://owasp.org/www-project-top-ten/"]
    }
