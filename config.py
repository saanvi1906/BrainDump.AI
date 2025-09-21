from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./braindump.db"
    SUPERMEMORY_API_KEY: str = ""
    LLM_MODEL: str = "gemma3:1b"
    APP_CORS_ORIGINS: str = "*"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
