import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    COGNODB_URI: str = os.getenv("COGNODB_URI", "bolt+s://localhost:7687")
    COGNODB_USER: str = os.getenv("COGNODB_USER", "cognodb")
    COGNODB_PASSWORD: str = os.getenv("COGNODB_PASSWORD", "")
    APP_PORT: int = int(os.getenv("PORT", 8000))
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*",
        "*"
    ]

settings = Settings()