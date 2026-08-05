import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Root Directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
SERVER_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from root or server directory
load_dotenv(dotenv_path=BASE_DIR / ".env")
load_dotenv(dotenv_path=SERVER_DIR / "app" / ".env")

class Settings(BaseModel):
    PROJECT_NAME: str = "MediGuru AI Document Intelligence"
    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: [
        origin.strip() for origin in os.environ.get("ALLOWED_ORIGINS", "*").split(",")
    ])
    
    # API Keys
    GEMINI_API_KEY: str | None = Field(default_factory=lambda: os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
    GOOGLE_API_KEY: str | None = Field(default_factory=lambda: os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
    MISTRAL_API_KEY: str | None = Field(default_factory=lambda: os.environ.get("MISTRAL_API_KEY"))
    
    # Temporary Session Storage Directories
    TEMP_DIR: Path = Field(default_factory=lambda: BASE_DIR / "temp")
    UPLOAD_DIR: Path = Field(default_factory=lambda: BASE_DIR / "temp" / "uploads")
    CHROMA_DB_DIR: Path = Field(default_factory=lambda: BASE_DIR / "temp" / "chroma")
    
    # Upload Hardening Limits
    MAX_FILE_SIZE_BYTES: int = Field(default_factory=lambda: int(os.environ.get("MAX_FILE_SIZE_BYTES", str(20 * 1024 * 1024))))  # 20MB
    MIN_IMAGE_DIMENSION: int = 50      # min 50x50 pixels
    MAX_IMAGE_DIMENSION: int = 10000   # max 10000x10000 pixels

    # OCR Flags
    USE_MKLDNN: str = Field(default_factory=lambda: os.environ.get("FLAGS_use_mkldnn", "0"))

    model_config = {
        "arbitrary_types_allowed": True
    }

settings = Settings()

# Ensure directories exist
settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# Apply system environment configurations at initialization
os.environ['FLAGS_use_mkldnn'] = settings.USE_MKLDNN
if settings.GOOGLE_API_KEY and not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
