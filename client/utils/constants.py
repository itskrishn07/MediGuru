import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")

# App Brand Metadata
APP_NAME: str = "MediGuru"
APP_TAGLINE: str = "AI-Powered Medical Document Intelligence & Clinical Data Platform"
COMPANY_NAME: str = "MedAI Analyzer Pro"

# Color Palette Constants
COLOR_PRIMARY: str = "#0055D4"       # Medical Electric Blue
COLOR_PRIMARY_HOVER: str = "#0044AB" # Darker Blue Hover
COLOR_SECONDARY: str = "#FFFFFF"     # Clean White
COLOR_ACCENT: str = "#10B981"        # Emerald Green
COLOR_BG: str = "#F8FAFC"            # Slate 50 Light Background
COLOR_TEXT_MAIN: str = "#0F172A"     # Slate 900
COLOR_TEXT_MUTED: str = "#64748B"    # Slate 500
COLOR_BORDER: str = "#E2E8F0"        # Slate 200

# File Upload Constraints
MAX_FILE_SIZE_MB: int = 25
ALLOWED_EXTENSIONS: list[str] = ["pdf", "png", "jpg", "jpeg"]
