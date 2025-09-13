from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Configuration for the application, loaded from environment variables.
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    database_url: str
    llm_api_key: str
    llm_mock_enabled: bool = True
    llm_model: str


settings = Settings()
