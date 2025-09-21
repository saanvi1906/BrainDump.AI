from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_SECRET: str = os.getenv("APP_SECRET", "change-me")
    APP_CORS_ORIGINS: list[str] = os.getenv("APP_CORS_ORIGINS", "").split(",") if os.getenv("APP_CORS_ORIGINS") else ["*"]
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./braindumb.db")

    SUPERMEMORY_API_BASE: str = os.getenv("SUPERMEMORY_API_BASE", "")
    SUPERMEMORY_API_KEY: str = os.getenv("SUPERMEMORY_API_KEY", "")
    SUPERMEMORY_SPACE_ID: str = os.getenv("SUPERMEMORY_SPACE_ID", "")

settings = Settings()
