from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./braindump.db"
    SUPERMEMORY_API_KEY: str ="sm_JuRF4dhaRY4p6LYRYR6D7t_GvyHEDeffXcvHTjZJPFxCfOjkGjHotWVGaUVAkMOxRnLsQyvgyiygSZzVphSqBbk"
    LLM_MODEL: str = "llama3.1:8b"          
    APP_CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
