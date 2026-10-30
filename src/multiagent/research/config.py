"""Environment configuration for the research assistant."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[3] / ".env")

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

_PLACEHOLDERS = {"", "api_key", "your_api_key_here", "your_openai_api_key_here"}


def require_api_key() -> str:
    """Return the OpenAI API key, or exit with a clear message if it is missing."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key.lower() in _PLACEHOLDERS:
        sys.exit(
            "ERROR: OPENAI_API_KEY is missing or still a placeholder in .env\n"
            "Get a key at https://platform.openai.com/api-keys and set it in .env"
        )
    return api_key
