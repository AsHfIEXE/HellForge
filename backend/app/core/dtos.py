import uuid
import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ScanContext(BaseModel):
    scan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = "default-project-uuid"
    target_domain: str
    started_by: str = "system"
    config: Dict[str, Any] = Field(default_factory=dict)
    statistics: Dict[str, int] = Field(default_factory=dict)

class AssetEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    scan_id: str
    domain: str
    subdomain: str
    ip_address: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    discovery_source: str = "subfinder"
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

class HTTPEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subdomain: str
    port: int = 443
    status_code: int = 200
    title: Optional[str] = None
    server_header: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    waf_detected: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

class FindingEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subdomain: str
    title: str
    severity: str # Critical, High, Medium, Low, Info
    category: str
    description: str
    remediation: Optional[str] = None
    cvss_score: float = 0.0
    cve_id: Optional[str] = None
    discovery_source: str = "nuclei"
    timestamp: str = Field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

class RiskEvent(BaseModel):
    subdomain: str
    risk_score: float
    rating: str
    breakdown: Dict[str, float]
