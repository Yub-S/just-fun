from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):
    DATABASE_URL:str
    JWT_KEY:str
    JWT_ALGORITHM:str
    REDIS_HOST:str
    REDIS_PORT:int=6379
    REDIS_URL:str="redis://localhost:6379/0" # "redis://127.0.0.1:6379/0"

    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM_NAME:str
    MAIL_STARTTLS:bool=True
    MAIL_SSL_TLS:bool=False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS:bool =True
    DOMAIN:str

    model_config = SettingsConfigDict(
        env_file="src/.env",
        extra="ignore"
    )

# create the object
Config = settings()

#celery configuration
broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup=True