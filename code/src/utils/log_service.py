import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
import os
import pandas as pd

class LogService:
    def __init__(self):
        """Initialize the Log Service."""
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
            
        # Set up file handler
        log_file = os.path.join(self.logs_dir, "app.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
    
    def log_event(self, level: str, message: str, component: str = "system", **kwargs) -> None:
        """
        Log an event with additional context
        Args:
            level: Log level (INFO, WARNING, ERROR, etc.)
            message: Log message
            component: Component generating the log
            **kwargs: Additional context to include in the log
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'component': component,
            **kwargs
        }
        
        # Log to file
        self.logger.log(getattr(logging, level.upper()), message)
        
        # Save to JSON log file
        self._save_to_json_log(log_entry)
    
    def get_logs(self, application: str = "all", server: str = "all", start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
        """
        Get logs with optional filtering
        Args:
            application: Application name to filter by
            server: Server name to filter by
            start_time: Start time for filtering
            end_time: End time for filtering
        Returns:
            List of log entries
        """
        try:
            # Load logs from file
            if not os.path.exists(self.log_file):
                return []
                
            with open(self.log_file, 'r') as f:
                logs = [json.loads(line) for line in f]
            
            # Apply filters
            filtered_logs = []
            for log in logs:
                # Convert log timestamp to datetime if it's a string
                log_timestamp = log.get('timestamp')
                if isinstance(log_timestamp, str):
                    try:
                        log_timestamp = datetime.fromisoformat(log_timestamp)
                    except ValueError:
                        continue
                
                # Apply time filters
                if start_time and log_timestamp < start_time:
                    continue
                if end_time and log_timestamp > end_time:
                    continue
                
                # Apply application and server filters
                if application != "all" and log.get('application') != application:
                    continue
                if server != "all" and log.get('server') != server:
                    continue
                
                filtered_logs.append(log)
            
            return filtered_logs
            
        except Exception as e:
            self.logger.error(f"Error getting logs: {str(e)}")
            return []
    
    def get_log_statistics(self, 
                          start_time: datetime = None, 
                          end_time: datetime = None) -> Dict[str, Any]:
        """
        Get statistics about logs
        Args:
            start_time: Start time for statistics
            end_time: End time for statistics
        Returns:
            Dictionary containing log statistics
        """
        try:
            logs = self.get_logs(start_time=start_time, end_time=end_time)
            
            if not logs:
                return {
                    'total_logs': 0,
                    'log_levels': {},
                    'components': {},
                    'time_range': None
                }
            
            # Calculate statistics
            df = pd.DataFrame(logs)
            
            # Convert timestamp strings to datetime objects if needed
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            stats = {
                'total_logs': len(logs),
                'log_levels': df['level'].value_counts().to_dict(),
                'components': df['component'].value_counts().to_dict(),
                'time_range': {
                    'start': df['timestamp'].min().isoformat() if not df['timestamp'].empty else None,
                    'end': df['timestamp'].max().isoformat() if not df['timestamp'].empty else None
                }
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error calculating log statistics: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _save_to_json_log(self, log_entry: Dict[str, Any]) -> None:
        """Save a log entry to the JSON log file"""
        try:
            log_file = os.path.join(self.logs_dir, "logs.json")
            
            # Read existing logs
            logs = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            
            # Append new log entry
            logs.append(log_entry)
            
            # Write back to file
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving to JSON log: {str(e)}")
    
    def _read_json_logs(self) -> List[Dict[str, Any]]:
        """Read logs from the JSON log file"""
        try:
            log_file = os.path.join(self.logs_dir, "logs.json")
            
            if not os.path.exists(log_file):
                return []
            
            with open(log_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error reading JSON logs: {str(e)}")
            return [] 