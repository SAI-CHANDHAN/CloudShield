"""Configuration for the Gemini investigation pipeline."""

import logging
import os
from pathlib import Path

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"

LOGGER = logging.getLogger("cloudshield.ai_rag")
