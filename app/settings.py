import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "frameworks_raw.jsonl"
SOURCES_PATH = BASE_DIR / "scripts" / "framework_sources.json"


SYSTEM_PROMPT = """Ты — умный помощник, который помогает выбрать подходящий Python-фреймворк по описанию задачи.
Используй найденные сниппеты и предложи лучший вариант, объясни почему."""

CHROMA_DB_DIR = BASE_DIR / "data" / "chroma_db"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL")