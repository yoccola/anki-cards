"""Configuration settings for the Anki Cards Etymology Enhancer."""
from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).parent

# Default file paths
DEFAULT_ETYMOLOGY_CSV = BASE_DIR / "etymology_data.csv"
DEFAULT_INPUT_TSV = BASE_DIR / "toeic_vocabulary" / "english_words.tsv"
DEFAULT_OUTPUT_TSV = BASE_DIR / "toeic_vocabulary" / "english_words_updated.tsv"

# File encoding
DEFAULT_ENCODING = "utf-8"

# You can override these with environment variables
ETYMOLOGY_CSV = Path(os.environ.get("ANKI_ETYMOLOGY_CSV", DEFAULT_ETYMOLOGY_CSV))
INPUT_TSV = Path(os.environ.get("ANKI_INPUT_TSV", DEFAULT_INPUT_TSV))
OUTPUT_TSV = Path(os.environ.get("ANKI_OUTPUT_TSV", DEFAULT_OUTPUT_TSV))
ENCODING = os.environ.get("ANKI_ENCODING", DEFAULT_ENCODING)