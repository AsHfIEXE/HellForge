import re
from typing import Dict, List, Any

# Pattern definitions for secret mining & endpoint extraction
SECRET_PATTERNS = {
    "AWS Access Key": r"(?i)\b(AKIA[0-9A-Z]{16})\b",
    "AWS Secret Key": r"(?i)\b([0-9a-zA-Z/+]{40})\b",
    "JWT Token": r"eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
    "Bearer Token": r"(?i)bearer\s+[a-zA-Z0-9_\-\.=]+",
    "Generic API Key": r"(?i)(api_key|apikey|secret_key|api_secret)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{16,64})['\"]",
    "Firebase URL": r"https://[a-z0-9\-]+\.firebaseio\.com",
    "Internal Endpoint": r"/(?:api|v1|v2|v3|graphql|auth|admin|user|config|internal)/[a-zA-Z0-9_/\-]+"
}

class JSIntelAnalyzer:
    """
    Analyzes JavaScript source code to extract endpoints, API keys, JWTs, AWS credentials, and hidden routes.
    """
    @staticmethod
    def analyze_script(script_content: str) -> Dict[str, Any]:
        secrets_found = []
        endpoints_found = set()

        for secret_type, pattern in SECRET_PATTERNS.items():
            matches = re.findall(pattern, script_content)
            if matches:
                for match in set(matches):
                    val = match[1] if isinstance(match, tuple) else match
                    if secret_type == "Internal Endpoint":
                        endpoints_found.add(val)
                    else:
                        # Avoid duplicate noisy matches
                        if len(val) >= 8:
                            secrets_found.append({
                                "type": secret_type,
                                "value": val,
                                "snippet": script_content[max(0, script_content.find(val)-20):min(len(script_content), script_content.find(val)+len(val)+20)]
                            })

        return {
            "secrets": secrets_found,
            "endpoints": list(endpoints_found),
            "total_secrets": len(secrets_found),
            "total_endpoints": len(endpoints_found)
        }

js_analyzer = JSIntelAnalyzer()
