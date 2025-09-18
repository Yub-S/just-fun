from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):
    DATABASE_URL:str
    JWT_KEY:str
    JWT_ALGORITHM:str

    model_config = SettingsConfigDict(
        env_file="src/.env",
        extra="ignore"
    )

# create the object
Config = settings()