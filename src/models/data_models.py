from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import numpy as np
from pydantic import BaseModel

@dataclass
class IslamicSource:
    text: str
    source_type: str  # 'quran' or 'hadith'
    reference: str    # e.g., "2:275" for Quran or "Bukhari:1234" for hadith
    topics: List[str]
    principles: List[str]
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, str] = field(default_factory=dict)  # Map of verse references to their text

@dataclass
class ReasoningResult:
    question: str
    relevant_sources: List[IslamicSource]
    reasoning: str
    confidence_score: float
