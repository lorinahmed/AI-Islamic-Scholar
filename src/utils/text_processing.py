from transformers import AutoTokenizer, AutoModel
import torch
from config import EMBEDDING_MODEL

class TextProcessor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
        self.model = AutoModel.from_pretrained(EMBEDDING_MODEL)

    def generate_embedding(self, text: str) -> torch.Tensor:
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True,
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        return outputs.last_hidden_state.mean(dim=1).numpy()

    def preprocess_text(self, text: str) -> str:
        # Add text preprocessing logic here
        return text.strip().lower()
