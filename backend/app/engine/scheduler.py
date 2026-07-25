import datetime
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Subdomain, Finding

class ChangeDeltaTracker:
    """
    Compares historical scan assets and security findings to generate change deltas
    (+New Assets, +New Findings, -Removed Hosts).
    """
    @staticmethod
    def calculate_delta(
        previous_assets: List[Dict[str, Any]],
        current_assets: List[Dict[str, Any]],
        previous_findings: List[Dict[str, Any]],
        current_findings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        
        prev_sub_names = {a["name"] for a in previous_assets}
        curr_sub_names = {a["name"] for a in current_assets}

        new_assets = list(curr_sub_names - prev_sub_names)
        removed_assets = list(prev_sub_names - curr_sub_names)

        prev_find_titles = {f["title"] for f in previous_findings}
        curr_find_titles = {f["title"] for f in current_findings}

        new_findings = list(curr_find_titles - prev_find_titles)

        return {
            "new_assets_count": len(new_assets),
            "removed_assets_count": len(removed_assets),
            "new_findings_count": len(new_findings),
            "new_assets": new_assets,
            "removed_assets": removed_assets,
            "new_findings": new_findings,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

delta_tracker = ChangeDeltaTracker()
