from app.main import app
from app.core.dtos import ScanContext, AssetEvent
from app.core.events import event_bus_manager
from app.plugins.loader import plugin_loader

print("[+] FastAPI App Instance Loaded Successfully")
print("[+] Pydantic Immutable DTO Contracts Loaded")
print(f"[+] Topic EventBus Channels: {list(event_bus_manager.channels.keys())}")
print("[+] Categorized Plugin Marketplace Loader Initialized")
