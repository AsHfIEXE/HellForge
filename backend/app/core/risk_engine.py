from typing import Dict, Any, List
from app.core.dtos import FindingEvent

class ExposureScorer:
    def score(self, is_internet_facing: bool) -> float:
        return 15.0 if is_internet_facing else 0.0

class CVEScorer:
    def score(self, severity: str) -> float:
        mapping = {"Critical": 35.0, "High": 25.0, "Medium": 15.0, "Low": 5.0}
        return mapping.get(severity, 0.0)

class TechnologyScorer:
    def score(self, technologies: List[str]) -> float:
        score = 0.0
        for tech in technologies:
            if "Apache" in tech or "PHP" in tech:
                score += 5.0
        return score

class AuthScorer:
    def score(self, auth_required: bool) -> float:
        return -10.0 if auth_required else 0.0

class ModularRiskEngine:
    def __init__(self):
        self.exposure_scorer = ExposureScorer()
        self.cve_scorer = CVEScorer()
        self.tech_scorer = TechnologyScorer()
        self.auth_scorer = AuthScorer()

    def calculate_asset_risk(
        self,
        base_score: float = 10.0,
        is_internet_facing: bool = True,
        findings: List[FindingEvent] = None,
        technologies: List[str] = None,
        auth_required: bool = False
    ) -> Dict[str, Any]:
        findings = findings or []
        technologies = technologies or []

        score = base_score
        score += self.exposure_scorer.score(is_internet_facing)
        score += self.tech_scorer.score(technologies)
        score += self.auth_scorer.score(auth_required)

        cve_max = 0.0
        for f in findings:
            cve_max = max(cve_max, self.cve_scorer.score(f.severity))
        score += cve_max

        final_score = min(max(round(score, 1), 0.0), 100.0)
        
        rating = "Low"
        if final_score >= 80:
            rating = "Critical"
        elif final_score >= 60:
            rating = "High"
        elif final_score >= 40:
            rating = "Medium"

        return {
            "risk_score": final_score,
            "rating": rating,
            "breakdown": {
                "base": base_score,
                "exposure": self.exposure_scorer.score(is_internet_facing),
                "cve_max": cve_max,
                "auth_mitigation": self.auth_scorer.score(auth_required)
            }
        }

risk_engine = ModularRiskEngine()
