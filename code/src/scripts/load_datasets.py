import pandas as pd
import requests
import os

def download_dataset(url: str, output_path: str):
    """Download dataset from URL and save to specified path"""
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

def setup_datasets():
    """Download and setup all required datasets"""
    datasets = {
        "incidents": "URL_TO_INCIDENT_DATASET",
        "jira": "URL_TO_JIRA_DATASET",
        "kb_articles": "URL_TO_KB_DATASET",
        "stack_overflow": "URL_TO_SO_DATASET",
        "syslog": "URL_TO_SYSLOG_DATASET",
        "prometheus": "URL_TO_PROMETHEUS_DATASET",
        "cmdb": "URL_TO_CMDB_DATASET",
        "network": "URL_TO_NETWORK_DATASET"
    }

    for name, url in datasets.items():
        output_path = f"data/{name}_dataset.csv"
        os.makedirs("data", exist_ok=True)
        download_dataset(url, output_path)

if __name__ == "__main__":
    setup_datasets() 