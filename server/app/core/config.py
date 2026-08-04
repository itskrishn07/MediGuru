import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Base Directory (server/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from the .env file in server/app/ or server/
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if not ENV_PATH.exists():
    ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Settings(BaseModel):
    # App Settings
    PROJECT_NAME: str = "MediGuru"
    API_V1_STR: str = ""
    
    # API Keys
    GEMINI_API_KEY: str | None = Field(default_factory=lambda: os.environ.get("GEMINI_API_KEY"))
    GOOGLE_API_KEY: str | None = Field(default_factory=lambda: os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
    MISTRAL_API_KEY: str | None = Field(default_factory=lambda: os.environ.get("MISTRAL_API_KEY"))
    
    # Paths
    UPLOAD_DIR: Path = Field(default_factory=lambda: BASE_DIR / "uploads")
    CHROMA_DB_DIR: Path = Field(default_factory=lambda: BASE_DIR / "chroma_db")
    
    # Database
    DATABASE_URL: str = Field(default_factory=lambda: os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mediguru"))
    
    # Security & JWT
    JWT_SECRET: str = Field(default_factory=lambda: os.environ.get("JWT_SECRET", "9f82d1c68f12a34b2e67c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9"))
    JWT_ALGORITHM: str = Field(default_factory=lambda: os.environ.get("JWT_ALGORITHM", "HS256"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default_factory=lambda: int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default_factory=lambda: int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "7")))

    # OCR Flags
    USE_MKLDNN: str = Field(default_factory=lambda: os.environ.get("FLAGS_use_mkldnn", "0"))

    model_config = {
        "arbitrary_types_allowed": True
    }

settings = Settings()

# Apply system environment configurations at initialization
os.environ['FLAGS_use_mkldnn'] = settings.USE_MKLDNN
if settings.GOOGLE_API_KEY and not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

