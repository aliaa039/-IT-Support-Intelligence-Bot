"""
Central configuration for IT Support Intelligence Bot.
Uses environment variables with sensible defaults for local/free usage.
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # run: pip install -r requirements.txt

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database
DB_NAME = os.getenv("DB_NAME", "support_tickets.db")
DATABASE_PATH = DATA_DIR / DB_NAME

# LLM: "groq" (free cloud) or "ollama" (100% local, no API key)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower().strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

# Ollama (local - no key needed)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Roles
SUPPORT_ROLES = ["Support Agent", "Team Lead", "Manager"]
