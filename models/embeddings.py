import chromadb
import os
import numpy as np
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """Manage document embeddings for retrieval"""
    
    def __init__(self, model_name="all-MiniLM-L6-v2", persist_dir="data/vector_store"):
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer(model_name)
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            raise
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embeddings for a single text"""
        if not text:
            return np.zeros(384)  # Default embedding size for all-MiniLM-L6-v2
        
        try:
            return self.embedding_model.encode(text)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return np.zeros(384)
    
    def index_documents(self, documents: List[Dict[str, Any]], collection_name: str) -> bool:
        """Index parsed documents in ChromaDB"""
        try:
            # Get or create collection
            try:
                collection = self.client.get_collection(name=collection_name)
            except:
                collection = self.client.create_collection(name=collection_name)
            
            # Prepare documents for indexing
            doc_ids = []
            doc_texts = []
            doc_metadata = []
            
            for i, doc in enumerate(documents):
                # Combine sections into single text
                sections = doc.get("sections", {})
                full_text = "\n\n".join([sections.get(section, "") for section in sections.keys()])
                
                # Skip if no meaningful text
                if len(full_text.strip()) < 100:
                    continue
                
                doc_ids.append(f"doc_{i}")
                doc_texts.append(full_text)
                doc_metadata.append({
                    "file_path": doc.get("metadata", {}).get("file_path", ""),
                    "doc_type": doc.get("metadata", {}).get("doc_type", "Unknown"),
                    "filing_date": doc.get("metadata", {}).get("filing_date", "Unknown")
                })
            
            # Add documents to collection
            if doc_ids:
                collection.add(
                    ids=doc_ids,
                    documents=doc_texts,
                    metadatas=doc_metadata
                )
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            return False
