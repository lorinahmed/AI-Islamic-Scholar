from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.models.data_models import IslamicSource, ReasoningResult
from typing import List
import json

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Define paths relative to project root
QURAN_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'quran.json')
FAISS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'faiss_store')
FAISS_VERSION = "1.1"  # Increment this when metadata structure changes

class ReasoningEngine:
    def __init__(self):
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        
        # Create vector store using FAISS
        self.vector_store = self._initialize_vector_store()
        
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            max_tokens=1000,
            model="gpt-4",
            temperature=0.2,
        )
        
        # Create RAG chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={
                "prompt": self._create_reasoning_template()
            }
        )

    def _create_reasoning_template(self) -> PromptTemplate:
        template = """
        Question: {question}
        
        Relevant Islamic Sources:
        {context}
        
        IMPORTANT: Only use the sources provided above. Do not use any other knowledge.
        Even if the sources do not directly address the question, use Islamic principles and analogical reasoning (Qiyas) to derive an answer.
        
        Please reason about this question following these steps:
        1. Extract key principles from the provided sources
        2. Consider the context of each verse (surrounding verses and chapter theme)
        3. Apply analogical reasoning (Qiyas):
          - What are the underlying principles in these verses?
          - How do these principles apply to the current situation?
          - What similarities exist between the situations?
          - What would achieve the same purpose in today's context?
        4. Consider the broader objectives (Maqasid):
          - How does this relate to preserving faith, life, intellect, family, or property?
          - What promotes benefit and prevents harm?
        5. Provide evidence for your reasoning, explaining how the principles apply
        
        Remember:
        - Use analogical reasoning even when verses don't directly address the topic
        - Consider the spirit and purpose of the verses, not just literal meanings
        - Quote specific verses when making a point
        - Clearly state your reasoning process
        - Acknowledge uncertainty when present
        
        End with a clear conclusion in this format:
        
          CONCLUSION: [State whether the action is Halal/Haram/Makruh/Cannot be determined]
          CONFIDENCE: [High/Medium/Low] based on strength of analogical reasoning
          
          Allah knows best.
        
        Reasoning:
        """
        
        return PromptTemplate(
            template=template,
            input_variables=["question", "context"]
        )

    def _initialize_vector_store(self):
        """Initialize FAISS vector store with Quran verses"""
        # Check if FAISS index exists
        index_file = os.path.join(FAISS_PATH, "index.faiss")
        version_file = os.path.join(FAISS_PATH, "version.txt")
        
        # Check if index exists and version matches
        if os.path.exists(index_file) and os.path.exists(version_file):
            with open(version_file, 'r') as f:
                stored_version = f.read().strip()
            
            if stored_version == FAISS_VERSION:
                print("Loading existing FAISS index...")
                try:
                    return FAISS.load_local(
                        folder_path=FAISS_PATH,
                        embeddings=self.embeddings,
                        index_name="index",
                        allow_dangerous_deserialization=True
                    )
                except Exception as e:
                    print(f"Error loading index: {e}. Creating new index...")
            else:
                print(f"Index version mismatch (stored: {stored_version}, current: {FAISS_VERSION}). Recreating index...")

        print("Creating new FAISS index...")
        # Delete old index if it exists
        if os.path.exists(FAISS_PATH):
            import shutil
            shutil.rmtree(FAISS_PATH)
        
        with open(QURAN_PATH, 'r', encoding='utf-8') as f:
            quran_data = json.load(f)
            
        # Process verses with context
        texts = []
        metadata = []
        verses = quran_data['verses']
        
        for i, verse in enumerate(verses):
            # Get chapter and verse numbers
            chapter, verse_num = verse['reference'].split(':')
            verse_num = verse_num.replace('verse_', '')
            
            # Get surrounding verses (2 before and 2 after)
            context_start = max(0, i - 2)
            context_end = min(len(verses), i + 3)
            context_verses = verses[context_start:context_end]
            
            # Store the main verse text
            main_text = verse['text']
            
            # Create context dictionary
            context_dict = {
                v['reference']: v['text']
                for v in context_verses
                if v['reference'] != verse['reference']
            }
            
            # Add to texts and metadata
            texts.append(main_text)  # Use main verse text for embedding
            metadata.append({
                'source_type': 'quran',
                'reference': verse['reference'],
                'chapter': chapter,
                'verse_number': verse_num,
                'context': context_dict,
                'topics': verse['topics'],
                'principles': verse['principles']
            })

        vector_store = FAISS.from_texts(
            texts,
            self.embeddings,
            metadatas=metadata
        )

        # Save the FAISS index
        print("Saving FAISS index...")
        os.makedirs(FAISS_PATH, exist_ok=True)
        vector_store.save_local(
            folder_path=FAISS_PATH,
            index_name="index"
        )
        
        # Save version
        with open(version_file, 'w') as f:
            f.write(FAISS_VERSION)

        return vector_store

    def reason(self, question: str) -> ReasoningResult:
        """Generate reasoning about a question using RAG"""
        # Use RAG to get answer
        result = self.qa_chain.invoke({"query": question})
        
        # Get relevant sources from the context
        relevant_docs = self.vector_store.similarity_search_with_score(question)
        
        # Debug logging
        print("\nDEBUG: First document content:")
        if relevant_docs:
            print(f"Metadata: {relevant_docs[0][0].metadata}")
            print(f"Content: {relevant_docs[0][0].page_content}")
        
        # Split content into lines for each document
        for doc, _ in relevant_docs:
            content_lines = doc.page_content.split('\n')
            doc.metadata['context_verses'] = content_lines  # Store all verses in metadata
        
        # Calculate confidence score based on similarity scores
        if not relevant_docs:
            confidence_score = 0.0
        else:
            # Get average similarity score of top matches
            similarity_scores = [score for _, score in relevant_docs]
            avg_similarity = sum(similarity_scores) / len(similarity_scores)
            
            # Number of highly relevant verses (similarity > 0.5)
            relevant_count = sum(1 for score in similarity_scores if score > 0.5)
            
            # Calculate confidence based on both factors
            confidence_score = min(1.0, (avg_similarity * 0.7 + (relevant_count / 5) * 0.3))
        
        relevant_sources = [
            IslamicSource(
                source_type=doc.metadata['source_type'],
                reference=doc.metadata['reference'],
                text=doc.page_content,  # This is now just the main verse text
                topics=doc.metadata['topics'],
                principles=doc.metadata['principles'],
                metadata=doc.metadata,
                context=doc.metadata['context']  # Use the stored context
            )
            for doc, score in relevant_docs
        ]
        
        return ReasoningResult(
            question=question,
            relevant_sources=relevant_sources,
            reasoning=result['result'],
            confidence_score=round(confidence_score, 2)
        )

    def _format_sources(self, sources: List[IslamicSource]) -> str:
        return "\n\n".join([f"{source.source_type} {source.reference}:\n{source.text}" for source in sources])
