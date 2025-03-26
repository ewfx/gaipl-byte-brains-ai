import random
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta

class TelemetryService:
    def __init__(self):
        # Initialize with sample metrics (in production, this would connect to real monitoring systems)
        self.metrics_data = self._initialize_sample_data()

    def _initialize_sample_data(self) -> Dict[str, pd.DataFrame]:
        """Initialize sample telemetry data"""
        # Create sample timestamp range
        now = datetime.now()
        timestamps = [now - timedelta(minutes=i) for i in range(60)]
        
        return {
            "cpu_usage": pd.DataFrame({
                "timestamp": timestamps,
                "value": [random.uniform(20, 80) for _ in range(60)],
                "metric": "CPU Usage (%)"
            }),
            "memory_usage": pd.DataFrame({
                "timestamp": timestamps,
                "value": [random.uniform(40, 90) for _ in range(60)],
                "metric": "Memory Usage (%)"
            }),
            "disk_usage": pd.DataFrame({
                "timestamp": timestamps,
                "value": [random.uniform(30, 70) for _ in range(60)],
                "metric": "Disk Usage (%)"
            })
        }

    def get_metrics(self, metric_name: str, time_range: str = "1h") -> pd.DataFrame:
        """Get metrics data for specified metric and time range"""
        return self.metrics_data.get(metric_name, pd.DataFrame())

    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get active alerts"""
        return [
            {
                "id": "ALT001",
                "severity": "critical",
                "title": "High CPU Usage",
                "description": "CPU usage above 80% threshold",
                "timestamp": datetime.now() - timedelta(minutes=5)
            },
            {
                "id": "ALT002",
                "severity": "warning",
                "title": "Memory Usage Warning",
                "description": "Memory usage approaching 90% threshold",
                "timestamp": datetime.now() - timedelta(minutes=15)
            }
        ]

    def get_ci_list(self) -> List[str]:
        """Get list of Configuration Items"""
        return [
            "web-server-01",
            "app-server-02",
            "database-01",
            "cache-server-01"
        ]

    def get_ci_details(self, ci_id: str) -> Dict[str, Any]:
        """Get details for specific CI"""
        return {
            "id": ci_id,
            "type": "server",
            "status": "active",
            "metrics": {
                "cpu": self.get_metrics("cpu_usage"),
                "memory": self.get_metrics("memory_usage"),
                "disk": self.get_metrics("disk_usage")
            }
        } 