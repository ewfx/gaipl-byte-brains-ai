import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from typing import List, Dict, Any
import openai
from config.config import Config

class VectorStore:
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path="./data/vectordb")
        
        # Initialize OpenAI embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=Config.OPENAI_API_KEY,
            model_name="text-embedding-ada-002"
        )
        
        # Initialize collections for different data types
        self.collections = {
            "incidents": self.client.get_or_create_collection(
                name="incidents",
                embedding_function=self.embedding_function
            ),
            "kb_articles": self.client.get_or_create_collection(
                name="kb_articles",
                embedding_function=self.embedding_function
            ),
            "stack_overflow": self.client.get_or_create_collection(
                name="stack_overflow",
                embedding_function=self.embedding_function
            ),
            "syslog": self.client.get_or_create_collection(
                name="syslog",
                embedding_function=self.embedding_function
            )
        }

    def add_documents(self, collection_name: str, documents: List[Dict[str, Any]]):
        """Add documents to specified collection"""
        collection = self.collections[collection_name]
        
        # Prepare documents for insertion
        ids = [str(i) for i in range(len(documents))]
        texts = [doc['text'] for doc in documents]
        metadatas = [
            {k: v for k, v in doc.items() if k != 'text'}
            for doc in documents
        ]
        
        # Add to collection
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )

    def search(self, collection_name: str, query: str, n_results: int = 5) -> List[Dict]:
        """Search for similar documents in specified collection"""
        collection = self.collections[collection_name]
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results 