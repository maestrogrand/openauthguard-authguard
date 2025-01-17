from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080
    port: int = 50041
    service_name: str = "AuthGuard"
    users_service_url: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
