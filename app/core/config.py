from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Thinkkash Python API"
    DEBUG: bool = True
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
