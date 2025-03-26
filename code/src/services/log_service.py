import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from typing import List, Dict, Optional
import os
from datasets import load_dataset
import logging

class LogService:
    def __init__(self):
        self.log_data = {}
        self.sample_data_path = "data/sample_logs"
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def load_sample_data(self, source: str = "huggingface") -> Dict:
        """Load sample log data from various sources"""
        try:
            if source == "huggingface":
                return self._load_from_huggingface()
            elif source == "kaggle":
                return self._load_from_kaggle()
            else:
                return self._generate_sample_data()
        except Exception as e:
            self.logger.error(f"Error loading sample data: {str(e)}")
            return self._generate_sample_data()

    def _load_from_huggingface(self) -> Dict:
        """Load sample log data from Hugging Face datasets"""
        try:
            # Try to load from Hugging Face
            dataset = load_dataset("logpai/loghub")
            # Convert to our format
            return self._convert_dataset_to_logs(dataset)
        except Exception as e:
            self.logger.warning(f"Failed to load from Hugging Face: {str(e)}")
            return self._generate_sample_data()
            
    def _load_from_kaggle(self) -> Dict:
        """Load sample log data from Kaggle datasets"""
        try:
            # Implementation for Kaggle dataset loading
            # This would require Kaggle API setup
            return self._generate_sample_data()
        except Exception as e:
            self.logger.warning(f"Failed to load from Kaggle: {str(e)}")
            return self._generate_sample_data()

    def _generate_sample_data(self) -> Dict:
        """Generate synthetic log data"""
        applications = ["web_server", "database", "auth_service", "api_gateway"]
        servers = ["server-01", "server-02", "server-03", "server-04"]
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        components = ["auth", "database", "api", "cache", "network", "security", "monitoring"]
        log_messages = [
            "User authentication successful",
            "Database connection established",
            "API request processed",
            "Cache miss occurred",
            "Memory usage high",
            "CPU utilization exceeded threshold",
            "Network latency increased",
            "Service health check failed",
            "Security scan completed",
            "Backup process started",
            "Configuration updated",
            "Service restarted"
        ]

        logs = {}
        for app in applications:
            logs[app] = {}
            for server in servers:
                logs[app][server] = []
                # Generate 100 log entries per server
                for _ in range(100):
                    timestamp = datetime.now() - timedelta(
                        hours=random.randint(0, 24),
                        minutes=random.randint(0, 60)
                    )
                    
                    # Generate log level with weighted distribution
                    level_weights = {
                        "INFO": 0.6,    # 60% INFO logs
                        "WARNING": 0.2,  # 20% WARNING logs
                        "ERROR": 0.15,   # 15% ERROR logs
                        "DEBUG": 0.05    # 5% DEBUG logs
                    }
                    level = random.choices(list(level_weights.keys()), 
                                         weights=list(level_weights.values()))[0]
                    
                    # Select component based on application
                    if app == "web_server":
                        component = random.choice(["api", "cache", "network"])
                    elif app == "database":
                        component = random.choice(["database", "cache", "monitoring"])
                    elif app == "auth_service":
                        component = random.choice(["auth", "security", "api"])
                    else:  # api_gateway
                        component = random.choice(["api", "network", "security"])
                    
                    log_entry = {
                        "timestamp": timestamp,
                        "level": level,
                        "message": random.choice(log_messages),
                        "server": server,
                        "application": app,
                        "component": component,
                        "trace_id": f"trace-{random.randint(1000, 9999)}",
                        "user_id": f"user-{random.randint(1, 100)}",
                        "duration_ms": random.randint(10, 1000),
                        "status_code": random.choice([200, 201, 400, 401, 403, 500])
                    }
                    logs[app][server].append(log_entry)

        return logs
        
    def _convert_dataset_to_logs(self, dataset) -> Dict:
        """Convert dataset to our log format"""
        logs = {}
        # Implementation for dataset conversion
        return logs
        
    def get_logs(self,
                 application: str,
                 server: str,
                 start_time: Optional[datetime] = None,
                 end_time: Optional[datetime] = None,
                 log_level: Optional[str] = None) -> List[Dict]:
        """Get logs for specific application and server with filters"""
        # Load or generate sample data if not already loaded
        if not self.log_data:
            self.log_data = self.load_sample_data()

        # Flatten the nested structure for easier filtering
        all_logs = []
        for app in self.log_data:
            for srv in self.log_data[app]:
                for log in self.log_data[app][srv]:
                    all_logs.append(log)

        # Apply filters
        filtered_logs = all_logs
        
        if application and application != "all":
            filtered_logs = [log for log in filtered_logs if log['application'] == application]
            
        if server and server != "all":
            filtered_logs = [log for log in filtered_logs if log['server'] == server]
            
        if log_level:
            filtered_logs = [log for log in filtered_logs if log['level'] == log_level]
            
        if start_time:
            filtered_logs = [log for log in filtered_logs if log['timestamp'] >= start_time]
            
        if end_time:
            filtered_logs = [log for log in filtered_logs if log['timestamp'] <= end_time]

        return sorted(filtered_logs, key=lambda x: x['timestamp'])
        
    def get_log_summary(self,
                       application: str,
                       server: str,
                       time_window: str = "1h") -> Dict:
        """Get summary statistics for logs"""
        # Get logs with current filters
        logs = self.get_logs(application, server)
        
        if not logs:
            return {
                "total_logs": 0,
                "error_count": 0,
                "warning_count": 0,
                "avg_response_time": 0,
                "status_codes": {},
                "log_levels": {},
                "components": {}
            }

        # Calculate statistics
        df = pd.DataFrame(logs)
        
        # Convert timestamp strings to datetime if needed
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate time window
        end_time = datetime.now()
        if time_window == "1h":
            start_time = end_time - timedelta(hours=1)
        elif time_window == "24h":
            start_time = end_time - timedelta(days=1)
        else:
            start_time = end_time - timedelta(hours=1)
            
        # Filter by time window
        df = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]
        
        return {
            "total_logs": len(df),
            "error_count": len(df[df['level'] == 'ERROR']),
            "warning_count": len(df[df['level'] == 'WARNING']),
            "avg_response_time": df['duration_ms'].mean() if 'duration_ms' in df.columns else 0,
            "status_codes": df['status_code'].value_counts().to_dict() if 'status_code' in df.columns else {},
            "log_levels": df['level'].value_counts().to_dict(),
            "components": df['component'].value_counts().to_dict() if 'component' in df.columns else {},
            "time_range": {
                "start": df['timestamp'].min().isoformat() if not df['timestamp'].empty else None,
                "end": df['timestamp'].max().isoformat() if not df['timestamp'].empty else None
            }
        }
        
    def _count_status_codes(self, logs: List[Dict]) -> Dict:
        """Count occurrences of status codes"""
        counts = {}
        for log in logs:
            status = log["status_code"]
            counts[status] = counts.get(status, 0) + 1
        return counts
        
    def _count_log_levels(self, logs: List[Dict]) -> Dict:
        """Count occurrences of log levels"""
        counts = {}
        for log in logs:
            level = log["level"]
            counts[level] = counts.get(level, 0) + 1
        return counts