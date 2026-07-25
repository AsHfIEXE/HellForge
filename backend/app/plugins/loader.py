import os
import sys
import importlib.util
import logging
from typing import Dict, List, Any
from app.plugins.sdk import BasePlugin
from app.core.dtos import ScanContext

logger = logging.getLogger("HellForge.CategorizedPluginLoader")

class CategorizedPluginLoader:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.plugins_root = os.path.join(base_dir, "plugins")
        self.categories = ["official", "community", "private"]
        self.loaded_plugins: Dict[str, BasePlugin] = {}

    async def discover_and_load(self, ctx: ScanContext):
        for cat in self.categories:
            cat_dir = os.path.join(self.plugins_root, cat)
            if not os.path.exists(cat_dir):
                os.makedirs(cat_dir, exist_ok=True)
                continue

            for folder in os.listdir(cat_dir):
                plugin_folder = os.path.join(cat_dir, folder)
                if os.path.isdir(plugin_folder):
                    main_py = os.path.join(plugin_folder, "main.py")
                    if os.path.exists(main_py):
                        try:
                            mod_key = f"plugins.{cat}.{folder}"
                            if mod_key in sys.modules:
                                module = sys.modules[mod_key]
                            else:
                                spec = importlib.util.spec_from_file_location(mod_key, main_py)
                                module = importlib.util.module_from_spec(spec)
                                sys.modules[mod_key] = module
                                spec.loader.exec_module(module)

                            for attr_name in dir(module):
                                attr = getattr(module, attr_name)
                                if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr is not BasePlugin:
                                    instance = attr()
                                    if instance.name not in self.loaded_plugins:
                                        await instance.initialize(ctx)
                                        self.loaded_plugins[instance.name] = instance
                                        logger.info(f"Loaded Plugin [{cat.upper()}]: {instance.name} v{instance.version}")

                        except Exception as e:
                            logger.error(f"Failed to load plugin {cat}/{folder}: {e}")


    def list_plugins(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": p.name,
                "version": p.version,
                "author": getattr(p.manifest, 'author', 'Community') if p.manifest else 'Core',
                "description": getattr(p.manifest, 'description', '') if p.manifest else '',
                "subscriptions": p.subscriptions,
                "enabled": True
            }
            for p in self.loaded_plugins.values()
        ]

plugin_loader = CategorizedPluginLoader()
