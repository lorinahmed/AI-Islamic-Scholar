import os
import requests
from pathlib import Path
import json

# Define paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
QURAN_FILE = DATA_DIR / "quran.json"
QURAN_URL = "https://raw.githubusercontent.com/lorin/mufti/main/data/quran.json"

def download_quran_data():
    """Download Quran data if it doesn't exist"""
    if QURAN_FILE.exists():
        print(f"Quran data already exists at {QURAN_FILE}")
        return
    
    print("Downloading Quran data...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    response = requests.get(QURAN_URL)
    response.raise_for_status()
    
    with open(QURAN_FILE, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=2)
    
    print(f"Downloaded Quran data to {QURAN_FILE}")

def main():
    try:
        download_quran_data()
        print("Data preparation complete!")
    except Exception as e:
        print(f"Error preparing data: {e}")
        raise

if __name__ == "__main__":
    main() 