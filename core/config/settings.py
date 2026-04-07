from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    notion_api_key: str = ""
    notion_version: str = "2022-06-28"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()