from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

# Find and load .env file
load_dotenv(find_dotenv())


class Settings(BaseSettings):

    model_config = SettingsConfigDict(extra='ignore')

    database_url: str
    llm_api_key: str
    llm_mock_enabled: bool = True
    llm_model: str
    llm_max_tokens: int
    llm_temperature: float


settings = Settings()  # type: ignore
