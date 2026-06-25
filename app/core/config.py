from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Tennis Analyzer API"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/tennis_analyzer"

    SECRET_KEY: str = "your-secret-key-change-in-production-make-it-long-and-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    ANTHROPIC_API_KEY: str = ""

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_BUCKET_NAME: str = "tennis-analyzer-videos"
    AWS_REGION: str = "us-east-1"

    class Config:
        env_file = ".env"

settings = Settings()
