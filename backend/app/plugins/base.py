from typing import Dict, Any, List
import abc

class BasePlugin(abc.ABC):
    name: str = "BasePlugin"
    version: str = "1.0.0"
    description: str = "Base class for HellForge plugins"
    author: str = "HellForge Team"
    enabled: bool = True

    @abc.abstractmethod
    async def run(self, target_domain: str) -> Dict[str, Any]:
        """
        Executes the plugin logic for the given target domain.
        Returns a dict with discovered assets, findings, and metadata.
        """
        pass
