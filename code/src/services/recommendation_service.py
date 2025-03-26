import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import json
import os
from scipy.fft import fft

class RecommendationService:
    def __init__(self):
        self.telemetry_service = None  # Will be initialized with TelemetryService
        self.incident_service = None   # Will be initialized with IncidentService
        self.recommendation_history = []
        self.pattern_models = {}
        self.accuracy_metrics = {}
        self._load_recommendation_history()
        self.recommendations = []
        self.telemetry_data = []
        self.incident_data = []
        self._initialize_sample_data()

    def _load_recommendation_history(self):
        """Load historical recommendations from file"""
        history_file = "data/recommendation_history.json"
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                self.recommendation_history = json.load(f)

    def _save_recommendation_history(self):
        """Save recommendation history to file"""
        history_file = "data/recommendation_history.json"
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        with open(history_file, 'w') as f:
            json.dump(self.recommendation_history, f)

    def _initialize_sample_data(self):
        """Initialize sample data for testing"""
        # Sample recommendations with more realistic data
        self.recommendations = [
            {
                "id": 1,
                "title": "Optimize Database Queries",
                "description": "High CPU usage detected in database operations. Consider optimizing queries and adding indexes.",
                "priority": "High",
                "type": "Performance",
                "impact": "Reduced system latency and improved user experience",
                "created_at": datetime.now() - timedelta(days=2),
                "status": "effective",  # Pre-implemented and effective
                "confidence": 0.85,
                "supporting_data": {
                    "metric": "cpu_usage",
                    "threshold": 80,
                    "current_value": 85,
                    "affected_systems": ["database_server_1", "database_server_2"]
                }
            },
            {
                "id": 2,
                "title": "Update Security Patches",
                "description": "Critical security patches available for system components.",
                "priority": "High",
                "type": "Security",
                "impact": "Enhanced system security and vulnerability protection",
                "created_at": datetime.now() - timedelta(days=1),
                "status": "implemented",  # Pre-implemented but not yet effective
                "confidence": 0.95,
                "supporting_data": {
                    "patches": ["CVE-2024-1234", "CVE-2024-5678"],
                    "affected_systems": ["web_server", "api_gateway"]
                }
            },
            {
                "id": 3,
                "title": "Scale Application Servers",
                "description": "Increasing memory usage trend detected. Consider scaling application servers.",
                "priority": "Medium",
                "type": "Performance",
                "impact": "Improved application stability and response times",
                "created_at": datetime.now() - timedelta(hours=12),
                "status": "active",
                "confidence": 0.75,
                "supporting_data": {
                    "metric": "memory_usage",
                    "threshold": 70,
                    "current_value": 75,
                    "trend": "increasing",
                    "affected_systems": ["app_server_1", "app_server_2"]
                }
            },
            {
                "id": 4,
                "title": "Implement Rate Limiting",
                "description": "High number of API requests detected. Consider implementing rate limiting to prevent overload.",
                "priority": "High",
                "type": "Security",
                "impact": "Improved API stability and security",
                "created_at": datetime.now() - timedelta(hours=6),
                "status": "effective",  # Pre-implemented and effective
                "confidence": 0.9,
                "supporting_data": {
                    "metric": "api_requests",
                    "threshold": 1000,
                    "current_value": 1200,
                    "affected_systems": ["api_gateway", "load_balancer"]
                }
            },
            {
                "id": 5,
                "title": "Optimize Cache Configuration",
                "description": "Low cache hit rate detected. Consider adjusting cache parameters and eviction policies.",
                "priority": "Medium",
                "type": "Performance",
                "impact": "Improved response times and reduced database load",
                "created_at": datetime.now() - timedelta(hours=3),
                "status": "active",
                "confidence": 0.8,
                "supporting_data": {
                    "metric": "cache_hit_rate",
                    "threshold": 70,
                    "current_value": 65,
                    "affected_systems": ["cache_server_1", "cache_server_2"]
                }
            },
            {
                "id": 6,
                "title": "Update SSL Certificates",
                "description": "SSL certificates for multiple domains are approaching expiration.",
                "priority": "High",
                "type": "Security",
                "impact": "Prevent service disruption and maintain secure connections",
                "created_at": datetime.now() - timedelta(hours=1),
                "status": "active",
                "confidence": 0.95,
                "supporting_data": {
                    "expiring_certificates": [
                        {"domain": "api.example.com", "expires_in": 15},
                        {"domain": "app.example.com", "expires_in": 20}
                    ]
                }
            },
            {
                "id": 7,
                "title": "Implement Circuit Breaker",
                "description": "Multiple service failures detected. Consider implementing circuit breaker pattern.",
                "priority": "High",
                "type": "Reliability",
                "impact": "Improved system resilience and graceful degradation",
                "created_at": datetime.now() - timedelta(minutes=30),
                "status": "effective",  # Pre-implemented and effective
                "confidence": 0.85,
                "supporting_data": {
                    "failed_services": ["payment_service", "auth_service"],
                    "failure_rate": 0.15,
                    "affected_systems": ["api_gateway", "service_mesh"]
                }
            },
            {
                "id": 8,
                "title": "Optimize Database Indexes",
                "description": "Slow query performance detected. Consider adding missing indexes.",
                "priority": "Medium",
                "type": "Performance",
                "impact": "Improved query performance and reduced database load",
                "created_at": datetime.now() - timedelta(minutes=15),
                "status": "active",
                "confidence": 0.8,
                "supporting_data": {
                    "slow_queries": [
                        {"query": "SELECT * FROM users WHERE status = 'active'", "execution_time": 2.5},
                        {"query": "SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '7 days'", "execution_time": 1.8}
                    ],
                    "affected_tables": ["users", "orders"]
                }
            }
        ]

        # Generate more realistic telemetry data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='H')
        self.telemetry_data = []
        
        # CPU usage data with some anomalies
        for date in dates:
            base_value = 50 + np.sin(date.hour * np.pi / 12) * 20  # Daily pattern
            if np.random.random() < 0.05:  # 5% chance of anomaly
                value = base_value + np.random.normal(0, 30)
            else:
                value = base_value + np.random.normal(0, 5)
            self.telemetry_data.append({
                "timestamp": date,
                "metric": "cpu_usage",
                "value": max(0, min(100, value))
            })
            
            # Memory usage data with increasing trend
            base_memory = 60 + (date - dates[0]).days * 0.5  # Slight increase over time
            memory_value = base_memory + np.random.normal(0, 5)
            self.telemetry_data.append({
                "timestamp": date,
                "metric": "memory_usage",
                "value": max(0, min(100, memory_value))
            })
            
            # API request rate data
            base_requests = 500 + np.sin(date.hour * np.pi / 12) * 200  # Daily pattern
            request_value = base_requests + np.random.normal(0, 50)
            self.telemetry_data.append({
                "timestamp": date,
                "metric": "api_requests",
                "value": max(0, request_value)
            })
            
            # Cache hit rate data
            base_hit_rate = 75 + np.sin(date.hour * np.pi / 12) * 10  # Daily pattern
            hit_rate_value = base_hit_rate + np.random.normal(0, 3)
            self.telemetry_data.append({
                "timestamp": date,
                "metric": "cache_hit_rate",
                "value": max(0, min(100, hit_rate_value))
            })

        # Generate more realistic incident data
        self.incident_data = []
        for d in range(30):
            for h in range(24):
                if np.random.random() < 0.05:  # 5% chance of incident per hour
                    incident_time = datetime.now() - timedelta(days=d, hours=h)
                    severity = np.random.choice(["high", "medium", "low"], p=[0.2, 0.5, 0.3])
                    incident_type = np.random.choice(["error", "warning", "performance"], p=[0.4, 0.4, 0.2])
                    affected_system = np.random.choice([
                        "web_server", "api_gateway", "database_server", "cache_server",
                        "payment_service", "auth_service", "load_balancer", "service_mesh"
                    ])
                    
                    self.incident_data.append({
                        "timestamp": incident_time,
                        "type": incident_type,
                        "severity": severity,
                        "affected_system": affected_system,
                        "description": f"Sample {incident_type} incident with {severity} severity affecting {affected_system}"
                    })

    def analyze_telemetry_patterns(self, metrics: pd.DataFrame) -> Dict[str, Any]:
        """Analyze telemetry data for patterns and anomalies"""
        results = {
            "patterns": [],
            "anomalies": [],
            "trends": [],
            "recommendations": []
        }

        # Detect anomalies using Isolation Forest
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(metrics[['value']])
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomalies = iso_forest.fit_predict(scaled_data)
        
        # Identify patterns
        for metric in metrics['metric'].unique():
            metric_data = metrics[metrics['metric'] == metric]
            
            # Trend analysis
            trend = np.polyfit(range(len(metric_data)), metric_data['value'], 1)[0]
            if abs(trend) > 0.1:
                results["trends"].append({
                    "metric": metric,
                    "trend": "increasing" if trend > 0 else "decreasing",
                    "strength": abs(trend)
                })

            # Pattern detection
            if len(metric_data) > 24:  # At least 24 data points
                # Detect seasonality
                fft_result = fft(metric_data['value'])
                frequencies = np.fft.fftfreq(len(metric_data))
                dominant_freq = frequencies[np.argmax(np.abs(fft_result[1:len(fft_result)//2])) + 1]
                
                if abs(dominant_freq) > 0.1:
                    results["patterns"].append({
                        "metric": metric,
                        "type": "seasonality",
                        "period": int(1/dominant_freq)
                    })

        # Generate recommendations based on patterns
        for pattern in results["patterns"]:
            if pattern["type"] == "seasonality":
                results["recommendations"].append({
                    "type": "capacity_planning",
                    "priority": "medium",
                    "description": f"Consider scaling resources based on {pattern['metric']} seasonality pattern",
                    "confidence": 0.8,
                    "supporting_data": {
                        "pattern": pattern,
                        "metrics": [pattern["metric"]]
                    }
                })

        return results

    def correlate_incidents(self, incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze and correlate incidents to identify patterns and root causes"""
        results = {
            "patterns": [],
            "root_causes": [],
            "impact_analysis": [],
            "recommendations": []
        }

        # Group incidents by type and severity
        incident_groups = {}
        for incident in incidents:
            key = (incident.get('type'), incident.get('severity'))
            if key not in incident_groups:
                incident_groups[key] = []
            incident_groups[key].append(incident)

        # Analyze patterns
        for (incident_type, severity), group in incident_groups.items():
            if len(group) >= 3:  # Pattern threshold
                time_diffs = []
                for i in range(1, len(group)):
                    time_diff = (group[i]['timestamp'] - group[i-1]['timestamp']).total_seconds()
                    time_diffs.append(time_diff)

                if np.std(time_diffs) < 3600:  # Less than 1 hour variance
                    results["patterns"].append({
                        "type": incident_type,
                        "severity": severity,
                        "frequency": np.mean(time_diffs),
                        "count": len(group)
                    })

        # Generate recommendations based on patterns
        for pattern in results["patterns"]:
            results["recommendations"].append({
                "type": "incident_prevention",
                "priority": "high" if pattern["severity"] == "critical" else "medium",
                "description": f"Implement preventive measures for {pattern['type']} incidents",
                "confidence": 0.85,
                "supporting_data": {
                    "pattern": pattern,
                    "affected_systems": [inc.get('affected_system') for inc in incidents if inc.get('type') == pattern['type']]
                }
            })

        return results

    def generate_proactive_recommendations(self) -> List[Dict[str, Any]]:
        """Generate proactive recommendations based on telemetry and incident data"""
        recommendations = []
        
        # Analyze telemetry data
        df = pd.DataFrame(self.telemetry_data)
        telemetry_analysis = self.analyze_telemetry_patterns(df)
        
        # Generate recommendations based on telemetry patterns
        for trend in telemetry_analysis["trends"]:
            if trend["strength"] > 0.5:
                recommendations.append({
                    "id": len(self.recommendations) + 1,
                    "title": f"Address {trend['metric']} Trend",
                    "description": f"Detected {trend['trend']} trend in {trend['metric']}. Consider proactive measures.",
                    "priority": "High" if trend["strength"] > 1.0 else "Medium",
                    "type": "Performance",
                    "impact": f"Prevent potential issues related to {trend['metric']}",
                    "created_at": datetime.now(),
                    "status": "active",
                    "confidence": 0.85,
                    "supporting_data": {
                        "trend": trend,
                        "metric": trend["metric"]
                    }
                })
        
        # Analyze incident patterns
        incident_df = pd.DataFrame(self.incident_data)
        if not incident_df.empty:
            # Group incidents by type and severity
            incident_patterns = incident_df.groupby(['type', 'severity']).size().reset_index(name='count')
            
            # Generate recommendations based on incident patterns
            for _, pattern in incident_patterns.iterrows():
                if pattern['count'] >= 5:
                    recommendations.append({
                        "id": len(self.recommendations) + 1,
                        "title": f"Address {pattern['type']} Incidents",
                        "description": f"High frequency of {pattern['severity']} severity {pattern['type']} incidents detected.",
                        "priority": "High" if pattern['severity'] == "high" else "Medium",
                        "type": "Reliability",
                        "impact": "Improved system stability and reduced incident frequency",
                        "created_at": datetime.now(),
                        "status": "active",
                        "confidence": 0.9,
                        "supporting_data": {
                            "incident_type": pattern['type'],
                            "severity": pattern['severity'],
                            "count": pattern['count']
                        }
                    })
        
        # Add new recommendations to the list
        self.recommendations.extend(recommendations)
        return recommendations

    def calculate_recommendation_accuracy(self, time_range: str = "30d") -> Dict[str, float]:
        """Calculate accuracy metrics for historical recommendations"""
        start_time = datetime.now() - timedelta(days=int(time_range[:-1]))
        
        # Filter recent recommendations
        recent_recs = [rec for rec in self.recommendation_history 
                      if datetime.fromisoformat(rec["timestamp"]) >= start_time]
        
        if not recent_recs:
            return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

        # Calculate metrics
        true_positives = sum(1 for rec in recent_recs if rec.get("was_effective", False))
        false_positives = sum(1 for rec in recent_recs if not rec.get("was_effective", False))
        false_negatives = sum(1 for rec in recent_recs if rec.get("was_implemented", False) and not rec.get("was_effective", False))

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        self.accuracy_metrics = {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "total_recommendations": len(recent_recs),
            "effective_recommendations": true_positives
        }

        return self.accuracy_metrics

    def get_recommendations(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get recommendations within the specified date range"""
        # Generate new proactive recommendations
        self.generate_proactive_recommendations()
        
        return [
            rec for rec in self.recommendations
            if start_date <= rec["created_at"] <= end_date
            and rec["status"] == "active"
        ]

    def mark_recommendation_implemented(self, recommendation_id: int) -> None:
        """Mark a recommendation as implemented"""
        for rec in self.recommendations:
            if rec["id"] == recommendation_id:
                rec["status"] = "implemented"
                # Update accuracy metrics
                self.get_accuracy_metrics()
                break

    def mark_recommendation_effective(self, recommendation_id: int) -> None:
        """Mark a recommendation as effective"""
        for rec in self.recommendations:
            if rec["id"] == recommendation_id:
                rec["status"] = "effective"
                # Update accuracy metrics
                self.get_accuracy_metrics()
                break

    def get_telemetry_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get telemetry data within the specified date range"""
        return [
            data for data in self.telemetry_data
            if start_date <= data["timestamp"] <= end_date
        ]

    def get_incident_patterns(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get incident patterns within the specified date range"""
        incidents = [
            data for data in self.incident_data
            if start_date <= data["timestamp"] <= end_date
        ]
        
        if not incidents:
            return []
            
        # Group incidents by hour and day
        df = pd.DataFrame(incidents)
        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.day
        df['count'] = 1
        
        # Group by day and hour, count incidents
        patterns = df.groupby(['day', 'hour'])['count'].sum().reset_index()
        
        # Create a complete grid of days and hours
        all_days = range(1, 32)  # Assuming max 31 days
        all_hours = range(24)
        
        # Create a complete DataFrame with all combinations
        complete_df = pd.DataFrame(
            [(day, hour) for day in all_days for hour in all_hours],
            columns=['day', 'hour']
        )
        
        # Merge with actual data, filling missing values with 0
        complete_df = complete_df.merge(
            patterns,
            on=['day', 'hour'],
            how='left'
        ).fillna(0)
        
        return complete_df.to_dict('records')

    def get_accuracy_metrics(self) -> Dict[str, float]:
        """Get detailed accuracy metrics"""
        # Get all recommendations
        total_recommendations = len(self.recommendations)
        
        # Get implemented recommendations (both implemented and effective)
        implemented = [r for r in self.recommendations if r["status"] in ["implemented", "effective"]]
        implemented_count = len(implemented)
        
        # Get effective recommendations
        effective = [r for r in self.recommendations if r["status"] == "effective"]
        effective_count = len(effective)
        
        if implemented_count == 0:
            return {
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "total_recommendations": total_recommendations,
                "implemented_count": implemented_count,
                "effective_count": effective_count
            }
        
        # Calculate metrics
        precision = effective_count / implemented_count
        recall = effective_count / total_recommendations
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "total_recommendations": total_recommendations,
            "implemented_count": implemented_count,
            "effective_count": effective_count
        }

    def update_recommendation_feedback(self, 
                                    recommendation_id: str, 
                                    was_effective: bool, 
                                    was_implemented: bool) -> bool:
        """Update recommendation feedback"""
        for rec in self.recommendation_history:
            if rec.get("id") == recommendation_id:
                rec["was_effective"] = was_effective
                rec["was_implemented"] = was_implemented
                rec["feedback_timestamp"] = datetime.now().isoformat()
                self._save_recommendation_history()
                return True
        return False 