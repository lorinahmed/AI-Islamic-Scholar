from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Data directories
DATA_DIR = BASE_DIR / "data"
QURAN_PATH = DATA_DIR / "quran.json"
HADITH_PATH = DATA_DIR / "hadith.json"

# Model configurations
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vector store configurations
VECTOR_DIMENSION = 768  # Depends on the embedding model