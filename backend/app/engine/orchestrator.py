import asyncio
import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Organization, Project, Target, Domain, Subdomain, Service, Finding, Scan, TimelineEvent
from app.core.dtos import ScanContext, AssetEvent, HTTPEvent, FindingEvent
from app.core.events import event_bus_manager
from app.core.risk_engine import risk_engine
from app.plugins.loader import plugin_loader

class ArchitectedOrchestrator:
    def __init__(self):
        self._assets_buffer: List[AssetEvent] = []
        self._http_buffer: List[HTTPEvent] = []
        self._findings_buffer: List[FindingEvent] = []

        # Hook DTO buffers to topic channels
        event_bus_manager.asset_bus.subscribe(self._on_asset_event)
        event_bus_manager.http_bus.subscribe(self._on_http_event)
        event_bus_manager.finding_bus.subscribe(self._on_finding_event)

    async def _on_asset_event(self, data: AssetEvent):
        if isinstance(data, AssetEvent):
            self._assets_buffer.append(data)

    async def _on_http_event(self, data: HTTPEvent):
        if isinstance(data, HTTPEvent):
            self._http_buffer.append(data)

    async def _on_finding_event(self, data: FindingEvent):
        if isinstance(data, FindingEvent):
            self._findings_buffer.append(data)

    async def run_pipeline(self, db: AsyncSession, domain_name: str) -> Scan:
        # Clear buffers
        self._assets_buffer.clear()
        self._http_buffer.clear()
        self._findings_buffer.clear()

        ctx = ScanContext(target_domain=domain_name)

        # Ensure Org, Project, Target
        org_res = await db.execute(select(Organization).where(Organization.name == "Default Organization"))
        org = org_res.scalars().first()
        if not org:
            org = Organization(name="Default Organization", description="Primary Security Sandbox")
            db.add(org)
            await db.commit()
            await db.refresh(org)

        proj_res = await db.execute(select(Project).where(Project.org_id == org.id, Project.name == "Default Project"))
        project = proj_res.scalars().first()
        if not project:
            project = Project(org_id=org.id, name="Default Project", description="Main Attack Surface Target List")
            db.add(project)
            await db.commit()
            await db.refresh(project)

        target_res = await db.execute(select(Target).where(Target.project_id == project.id, Target.name == domain_name))
        target = target_res.scalars().first()
        if not target:
            target = Target(project_id=project.id, name=domain_name)
            db.add(target)
            await db.commit()
            await db.refresh(target)

        dom_res = await db.execute(select(Domain).where(Domain.target_id == target.id, Domain.name == domain_name))
        domain_obj = dom_res.scalars().first()
        if not domain_obj:
            domain_obj = Domain(target_id=target.id, name=domain_name)
            db.add(domain_obj)
            await db.commit()
            await db.refresh(domain_obj)

        scan = Scan(id=ctx.scan_id, target_id=target.id, status="running", progress=10)
        db.add(scan)
        await db.commit()
        await db.refresh(scan)

        # Discover & Initialize Plugins with ScanContext
        await plugin_loader.discover_and_load(ctx)

        # Trigger Pipeline via topic bus scan channel
        await event_bus_manager.scan_bus.publish(ctx)
        
        await asyncio.sleep(0.8) # Wait for plugins topic message cascades
        scan.progress = 70

        # Persist DTOs to Database using Batch Operations
        sub_map = {}
        new_subdomains = []

        for asset_evt in self._assets_buffer:
            stmt = select(Subdomain).where(Subdomain.domain_id == domain_obj.id, Subdomain.name == asset_evt.subdomain)
            res = await db.execute(stmt)
            sub_rec = res.scalars().first()
            
            is_admin = "admin" in asset_evt.subdomain or "dev" in asset_evt.subdomain
            r_eval = risk_engine.calculate_asset_risk(
                base_score=15.0,
                is_internet_facing=True,
                auth_required=not is_admin
            )

            if not sub_rec:
                sub_rec = Subdomain(
                    domain_id=domain_obj.id,
                    name=asset_evt.subdomain,
                    risk_score=r_eval["risk_score"],
                    tags=asset_evt.tags,
                    discovery_source=asset_evt.discovery_source
                )
                new_subdomains.append(sub_rec)
            sub_map[asset_evt.subdomain] = sub_rec

        if new_subdomains:
            db.add_all(new_subdomains)
            await db.commit()

        # Batch Persist HTTP Services & Findings
        new_services = []
        new_findings = []

        for http_evt in self._http_buffer:
            sub_rec = sub_map.get(http_evt.subdomain)
            if sub_rec:
                svc_rec = Service(
                    subdomain_id=sub_rec.id,
                    port=http_evt.port,
                    service_name="https",
                    title=http_evt.title,
                    status_code=http_evt.status_code,
                    server_header=http_evt.server_header,
                    waf=http_evt.waf_detected,
                    technologies=http_evt.technologies
                )
                new_services.append(svc_rec)

                for f_evt in self._findings_buffer:
                    if f_evt.subdomain == http_evt.subdomain:
                        finding_rec = Finding(
                            service_id=svc_rec.id,
                            title=f_evt.title,
                            severity=f_evt.severity,
                            category=f_evt.category,
                            description=f_evt.description,
                            remediation=f_evt.remediation,
                            cvss_score=f_evt.cvss_score,
                            cve_id=f_evt.cve_id,
                            discovery_source=f_evt.discovery_source
                        )
                        new_findings.append(finding_rec)

        if new_services:
            db.add_all(new_services)
        if new_findings:
            db.add_all(new_findings)

        # Record Timeline Event
        timeline_ev = TimelineEvent(
            domain=domain_name,
            event_type="scan.finished",
            title=f"Scan Finished for {domain_name}",
            description=f"EventBus pipeline processed {len(self._assets_buffer)} assets and {len(self._findings_buffer)} security findings."
        )
        db.add(timeline_ev)

        # Finish Scan
        scan.status = "completed"
        scan.progress = 100
        scan.completed_at = datetime.datetime.utcnow()
        scan.summary = {
            "assets_discovered": len(self._assets_buffer),
            "findings_count": len(self._findings_buffer)
        }
        await db.commit()
        await db.refresh(scan)

        return scan


event_orchestrator = ArchitectedOrchestrator()

