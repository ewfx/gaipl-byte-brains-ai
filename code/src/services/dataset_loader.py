import pandas as pd
from utils.sample_data_generator import (
    generate_incident_data,
    generate_kb_articles,
    generate_telemetry_data
)

class DatasetLoader:
    def __init__(self):
        # Initialize sample datasets
        self._sample_data = {
            "incidents": generate_incident_data(),
            "kb_articles": generate_kb_articles(),
            "telemetry": generate_telemetry_data()
        }

    def load_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Load dataset from sample data"""
        if dataset_name not in self._sample_data:
            raise ValueError(f"Dataset {dataset_name} not found")
        
        return self._sample_data[dataset_name]

    def refresh_dataset(self, dataset_name: str) -> pd.DataFrame:
        """Refresh sample dataset"""
        if dataset_name == "incidents":
            self._sample_data[dataset_name] = generate_incident_data()
        elif dataset_name == "kb_articles":
            self._sample_data[dataset_name] = generate_kb_articles()
        elif dataset_name == "telemetry":
            self._sample_data[dataset_name] = generate_telemetry_data()
        
        return self._sample_data[dataset_name] 