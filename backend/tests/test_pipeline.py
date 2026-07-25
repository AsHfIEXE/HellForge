import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.engine.orchestrator import event_orchestrator

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def async_db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_full_scan_pipeline_execution(async_db):
    scan = await event_orchestrator.run_pipeline(async_db, "testtarget.com")
    assert scan is not None
    assert scan.status == "completed"
    assert scan.progress == 100
    assert scan.summary["assets_discovered"] > 0
    assert scan.summary["findings_count"] > 0
