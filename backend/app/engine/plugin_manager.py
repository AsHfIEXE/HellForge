from typing import List, Dict, Type
from app.plugins.base import BasePlugin
from app.plugins.subdomain_enum import SubdomainDiscoveryPlugin
from app.plugins.http_intel import HTTPIntelPlugin
from app.plugins.secret_hunter import SecretHunterPlugin

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}
        self.register_default_plugins()

    def register_default_plugins(self):
        defaults = [
            SubdomainDiscoveryPlugin(),
            HTTPIntelPlugin(),
            SecretHunterPlugin()
        ]
        for p in defaults:
            self._plugins[p.name] = p

    def get_plugins(self) -> List[Dict]:
        return [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "author": p.author,
                "enabled": p.enabled
            }
            for p in self._plugins.values()
        ]

    def get_plugin(self, name: str) -> BasePlugin:
        return self._plugins.get(name)

plugin_manager = PluginManager()
