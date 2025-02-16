import os
import json
import numpy as np
from typing import List
from src.models.data_models import IslamicSource
from config import VECTOR_DIMENSION
from src.utils.text_processing import TextProcessor
from tqdm import tqdm

# Define paths relative to project root
QURAN_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'quran.json')
EMBEDDINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'embeddings.npz')

class VectorStore:
    def __init__(self):
        self.sources = []
        self.embeddings = []
        self.text_processor = TextProcessor()

    def load_initial_data(self):
        """Load initial data from JSON files"""
        # Check if embeddings already exist
        if os.path.exists(EMBEDDINGS_PATH):
            print("Loading pre-computed embeddings...")
            # Load sources and embeddings
            with open(QURAN_PATH, 'r', encoding='utf-8') as f:
                quran_data = json.load(f)
                self.sources = [IslamicSource(**verse) for verse in quran_data['verses']]
            
            # Load numpy array of embeddings
            loaded = np.load(EMBEDDINGS_PATH)
            self.embeddings = loaded['embeddings']
            return

        # Load Quran data and compute embeddings
        with open(QURAN_PATH, 'r', encoding='utf-8') as f:
            quran_data = json.load(f)
            print("Processing verse embeddings...")
            for verse in tqdm(quran_data['verses']):
                # Create source object
                source = IslamicSource(**verse)
                # Generate and store embedding
                embedding = self.text_processor.generate_embedding(verse['text'])
                # Ensure embedding is 1D
                embedding = embedding.squeeze()
                self.sources.append(source)
                self.embeddings.append(embedding)
        
        # Save embeddings to file
        print("Saving embeddings for future use...")
        np.savez(EMBEDDINGS_PATH, embeddings=np.array(self.embeddings))

    def add_embedding(self, embedding: np.ndarray):
        """Add an embedding to the store"""
        self.embeddings.append(embedding)

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[IslamicSource]:
        """Search for most similar sources based on embedding"""
        if len(self.embeddings) == 0:
            return []

        # Ensure query embedding is 1D
        query_embedding = query_embedding.squeeze()
        
        # Convert embeddings to numpy array for efficient computation
        embeddings_array = self.embeddings
        
        # Compute cosine similarity
        similarities = np.dot(embeddings_array, query_embedding) / (
            np.linalg.norm(embeddings_array, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get indices of top k most similar
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Print similarity scores for debugging
        print("\nTop matching verses and their similarity scores:")
        for idx, source_idx in enumerate(top_indices):
            print(f"\nScore {similarities[source_idx]:.3f}:")
            print(f"Verse {self.sources[source_idx].reference}:")
            print(f"{self.sources[source_idx].text}")
        
        return [self.sources[i] for i in top_indices]
