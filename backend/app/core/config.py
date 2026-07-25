from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "HellForge"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite+aiosqlite:///./hellforge.db"
    SECRET_KEY: str = "hellforge-super-secret-key-change-in-production"

    class Config:
        case_sensitive = True

settings = Settings()
