import json
import os
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer, BertForSequenceClassification
import numpy as np
import requests
from pathlib import Path

# Define topics and principles as classification labels
TOPICS = [
    'faith', 'ethics', 'worship', 'law', 'society', 
    'family', 'economics', 'history', 'afterlife', 'prophets'
]

PRINCIPLES = [
    'divine_unity', 'justice', 'moral_conduct', 'knowledge',
    'compassion', 'accountability', 'moderation', 'brotherhood',
    'repentance', 'gratitude'
]

# Define paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
QURAN_FILE = DATA_DIR / "quran.json"
QURAN_URL = "https://raw.githubusercontent.com/lorin/mufti/main/data/quran.json"  # Replace with your data URL

class QuranClassifier:
    def __init__(self):
        # Use BERT instead of DeBERTa to avoid dependency issues
        model_name = "bert-base-uncased"
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(TOPICS) + len(PRINCIPLES),
            problem_type="multi_label_classification"
        )
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
    def classify_text(self, text, threshold=0.5):
        inputs = self.tokenizer(
            text,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.sigmoid(outputs.logits)
        
        predictions = predictions[0].cpu().numpy()
        topic_preds = predictions[:len(TOPICS)]
        principle_preds = predictions[len(TOPICS):]
        
        topics = [TOPICS[i] for i, pred in enumerate(topic_preds) if pred > threshold]
        principles = [PRINCIPLES[i] for i, pred in enumerate(principle_preds) if pred > threshold]
        
        return topics, principles

def load_raw_data():
    """Load raw data from file"""
    raw_data_path = 'data/raw_quran.json'
    
    if not os.path.exists(raw_data_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_data_path}. Please run download script first.")
    
    print("Loading raw data from file...")
    with open(raw_data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_with_classifier(raw_data):
    """Process raw data with the classifier"""
    classifier = QuranClassifier()
    processed_verses = []
    
    print("\nClassifying verses...")
    for verse in tqdm(raw_data['verses'], desc="Processing verses"):
        topics, principles = classifier.classify_text(verse['text'])
        processed_verse = verse.copy()
        processed_verse['topics'] = topics
        processed_verse['principles'] = principles
        processed_verses.append(processed_verse)
    
    return {'verses': processed_verses}

def download_quran_data():
    """Download Quran data if it doesn't exist"""
    if QURAN_FILE.exists():
        print(f"Quran data already exists at {QURAN_FILE}")
        return
    
    print("Downloading Quran data...")
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download the file
    response = requests.get(QURAN_URL)
    response.raise_for_status()  # Raise an error for bad status codes
    
    # Save the file
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