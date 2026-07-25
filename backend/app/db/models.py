import uuid
import datetime
from typing import Dict, Any, List
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

def gen_uuid() -> str:
    return str(uuid.uuid4())

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    projects = relationship("Project", back_populates="organization", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=gen_uuid)
    org_id = Column(String, ForeignKey("organizations.id"))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    organization = relationship("Organization", back_populates="projects")
    targets = relationship("Target", back_populates="project", cascade="all, delete-orphan")

class Target(Base):
    __tablename__ = "targets"

    id = Column(String, primary_key=True, default=gen_uuid)
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String, nullable=False) # e.g. example.com
    scope_type = Column(String, default="domain") # domain, cidr, ip
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="targets")
    domains = relationship("Domain", back_populates="target", cascade="all, delete-orphan")
    scans = relationship("Scan", back_populates="target", cascade="all, delete-orphan")

class Domain(Base):
    __tablename__ = "domains"

    id = Column(String, primary_key=True, default=gen_uuid)
    target_id = Column(String, ForeignKey("targets.id"))
    name = Column(String, nullable=False) # example.com
    registrar = Column(String, nullable=True)
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    target = relationship("Target", back_populates="domains")
    subdomains = relationship("Subdomain", back_populates="domain_rel", cascade="all, delete-orphan")

class Subdomain(Base):
    __tablename__ = "subdomains"

    id = Column(String, primary_key=True, default=gen_uuid)
    domain_id = Column(String, ForeignKey("domains.id"))
    name = Column(String, nullable=False) # api.example.com
    is_live = Column(Boolean, default=True)
    risk_score = Column(Float, default=10.0)
    tags = Column(JSON, default=list) # ["api", "admin", "cloud"]
    discovery_source = Column(String, default="subfinder")
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)

    domain_rel = relationship("Domain", back_populates="subdomains")
    ips = relationship("IPAddress", back_populates="subdomain", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="subdomain", cascade="all, delete-orphan")

class IPAddress(Base):
    __tablename__ = "ip_addresses"

    id = Column(String, primary_key=True, default=gen_uuid)
    subdomain_id = Column(String, ForeignKey("subdomains.id"))
    ip = Column(String, nullable=False)
    asn = Column(String, nullable=True)
    country = Column(String, nullable=True)
    is_cdn = Column(Boolean, default=False)
    cdn_provider = Column(String, nullable=True)

    subdomain = relationship("Subdomain", back_populates="ips")

class Service(Base):
    __tablename__ = "services"

    id = Column(String, primary_key=True, default=gen_uuid)
    subdomain_id = Column(String, ForeignKey("subdomains.id"))
    port = Column(Integer, nullable=False)
    protocol = Column(String, default="tcp")
    service_name = Column(String, default="http") # http, https, ssh, mysql
    title = Column(String, nullable=True)
    status_code = Column(Integer, nullable=True)
    server_header = Column(String, nullable=True)
    waf = Column(String, nullable=True)
    technologies = Column(JSON, default=list)

    subdomain = relationship("Subdomain", back_populates="services")
    findings = relationship("Finding", back_populates="service", cascade="all, delete-orphan")

class Finding(Base):
    __tablename__ = "findings"

    id = Column(String, primary_key=True, default=gen_uuid)
    service_id = Column(String, ForeignKey("services.id"))
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False) # Critical, High, Medium, Low, Info
    category = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    remediation = Column(Text, nullable=True)
    cvss_score = Column(Float, default=0.0)
    cve_id = Column(String, nullable=True)
    discovery_source = Column(String, default="nuclei")
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)

    service = relationship("Service", back_populates="findings")
    evidence = relationship("Evidence", back_populates="finding", cascade="all, delete-orphan")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, default=gen_uuid)
    finding_id = Column(String, ForeignKey("findings.id"))
    request = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    extracted_secret = Column(String, nullable=True)
    screenshot_url = Column(String, nullable=True)

    finding = relationship("Finding", back_populates="evidence")

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, default=gen_uuid)
    target_id = Column(String, ForeignKey("targets.id"))
    status = Column(String, default="queued") # queued, running, completed, failed
    progress = Column(Integer, default=0)
    summary = Column(JSON, default=dict)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    target = relationship("Target", back_populates="scans")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=gen_uuid)
    action = Column(String, nullable=False)
    actor = Column(String, default="system")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(String, primary_key=True, default=gen_uuid)
    domain = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ScanSchedule(Base):
    __tablename__ = "scan_schedules"

    id = Column(String, primary_key=True, default=gen_uuid)
    target_domain = Column(String, nullable=False)
    cron_expression = Column(String, default="0 0 * * *") # Daily
    active = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=gen_uuid)
    target_domain = Column(String, nullable=False)
    format = Column(String, default="html") # html, markdown, json
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

class AssetDiff(Base):
    __tablename__ = "asset_diffs"

    id = Column(String, primary_key=True, default=gen_uuid)
    target_domain = Column(String, nullable=False)
    previous_scan_id = Column(String, nullable=True)
    current_scan_id = Column(String, nullable=False)
    delta_summary = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

