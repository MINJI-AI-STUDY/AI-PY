from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ai_port: int = Field(default=8000, validation_alias=AliasChoices("PORT", "AI_PORT"))
    google_api_key: SecretStr | None = Field(default=None, alias="GOOGLE_API_KEY")
    rag_top_k: int = Field(default=3, alias="RAG_TOP_K")


settings = Settings()
