import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory (server/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from the .env file in server/app/
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    # API Keys
    GEMINI_API_KEY: str | None = os.environ.get("GEMINI_API_KEY")
    GOOGLE_API_KEY: str | None = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    MISTRAL_API_KEY: str | None = os.environ.get("MISTRAL_API_KEY")
    
    # Paths
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    CHROMA_DB_DIR: Path = BASE_DIR / "chroma_db"
    
    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mediguru")
    
    # OCR Flags
    USE_MKLDNN: str = os.environ.get("FLAGS_use_mkldnn", "0")

settings = Settings()

# Apply system environment configurations at initialization
os.environ['FLAGS_use_mkldnn'] = settings.USE_MKLDNN
if settings.GOOGLE_API_KEY and not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
