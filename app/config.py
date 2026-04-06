from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ai_port: int = Field(default=8000, alias="AI_PORT")
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")


settings = Settings()
