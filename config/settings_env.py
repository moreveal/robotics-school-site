from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )
    
    SITE_NAME: str = "Digirobo"
    DEBUG: bool = True
    SECRET_KEY: str
    
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
