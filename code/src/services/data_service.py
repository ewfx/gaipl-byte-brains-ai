import pandas as pd
from services.dataset_loader import DatasetLoader
from services.vector_store import VectorStore
from typing import Dict, Any
from datetime import datetime, timedelta

class DataService:
    def __init__(self):
        self.dataset_loader = DatasetLoader()
        self.vector_store = VectorStore()
        self._cache: Dict[str, pd.DataFrame] = {}

    def initialize_vector_store(self):
        """Initialize vector store with all datasets"""
        # Load and process incidents
        incidents_df = self.get_dataset("incidents")
        self.vector_store.add_documents("incidents", [
            {
                'text': f"{row['title']}\n{row['description']}",
                'incident_id': row['id'],
                'priority': row['priority']
            }
            for _, row in incidents_df.iterrows()
        ])

        # Load and process Stack Overflow data
        stack_overflow_df = self.get_dataset("stack_overflow")
        self.vector_store.add_documents("stack_overflow", [
            {
                'text': f"{row['title']}\n{row['body']}",
                'post_id': row['id'],
                'tags': row['tags']
            }
            for _, row in stack_overflow_df.iterrows()
        ])

        # Load and process syslog data
        syslog_df = self.get_dataset("syslog")
        self.vector_store.add_documents("syslog", [
            {
                'text': row['message'],
                'timestamp': row['timestamp'],
                'severity': row['severity']
            }
            for _, row in syslog_df.iterrows()
        ])

    def search_similar_incidents(self, query: str, n_results: int = 5):
        """Search for similar incidents"""
        return self.vector_store.search("incidents", query, n_results)

    def search_kb_articles(self, query: str, n_results: int = 5):
        """Search for relevant KB articles"""
        return self.vector_store.search("kb_articles", query, n_results)

    def get_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Get dataset from cache or load it"""
        if dataset_name not in self._cache:
            self._cache[dataset_name] = self.dataset_loader.load_dataset(dataset_name)
        return self._cache[dataset_name]

    def refresh_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Refresh dataset in cache"""
        self._cache[dataset_name] = self.dataset_loader.refresh_dataset(dataset_name)
        return self._cache[dataset_name]

    def get_incidents(self, filters: Dict = None) -> pd.DataFrame:
        """Get incidents with optional filters"""
        incidents = self.get_dataset("incidents")
        if filters:
            for key, value in filters.items():
                incidents = incidents[incidents[key] == value]
        return incidents

    def get_kb_articles(self, search_query: str = None) -> pd.DataFrame:
        """Get knowledge base articles with optional search"""
        articles = self.get_dataset("kb_articles")
        if search_query:
            articles = articles[
                articles['title'].str.contains(search_query, case=False) |
                articles['content'].str.contains(search_query, case=False)
            ]
        return articles

    def get_telemetry(self, hours: int = 24) -> pd.DataFrame:
        """Get telemetry data for specified time range"""
        telemetry = self.get_dataset("telemetry")
        cutoff = datetime.now() - timedelta(hours=hours)
        return telemetry[telemetry['timestamp'] >= cutoff]

    def get_incident_data(self) -> pd.DataFrame:
        """Get incident dataset"""
        return self.get_dataset("incidents")

    def get_stack_overflow_data(self) -> pd.DataFrame:
        """Get Stack Overflow dataset"""
        return self.get_dataset("stack_overflow")

    def get_syslog_data(self) -> pd.DataFrame:
        """Get syslog dataset"""
        return self.get_dataset("syslog") 