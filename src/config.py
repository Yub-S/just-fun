from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):
    DATABASE_URL:str
    JWT_KEY:str
    JWT_ALGORITHM:str
    REDIS_HOST:str
    REDIS_PORT:int=6379

    model_config = SettingsConfigDict(
        env_file="src/.env",
        extra="ignore"
    )

# create the object
Config = settings()