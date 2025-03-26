from datetime import datetime, timedelta
from typing import List, Dict, Any

class AlertsService:
    def __init__(self):
        # Initialize with sample alerts (in production, this would connect to real alert systems)
        self._alerts = self._initialize_sample_alerts()

    def _initialize_sample_alerts(self) -> List[Dict[str, Any]]:
        """Initialize sample alerts data"""
        now = datetime.now()
        return [
            {
                "id": "ALT001",
                "severity": "critical",
                "title": "High CPU Usage",
                "description": "CPU usage above 80% threshold on web-server-01",
                "timestamp": now - timedelta(minutes=5),
                "status": "active",
                "ci_id": "web-server-01"
            },
            {
                "id": "ALT002",
                "severity": "warning",
                "title": "Memory Usage Warning",
                "description": "Memory usage approaching 90% threshold on app-server-02",
                "timestamp": now - timedelta(minutes=15),
                "status": "active",
                "ci_id": "app-server-02"
            },
            {
                "id": "ALT003",
                "severity": "info",
                "title": "Disk Space Alert",
                "description": "Disk usage above 75% on database-01",
                "timestamp": now - timedelta(minutes=30),
                "status": "active",
                "ci_id": "database-01"
            }
        ]

    def get_active_alerts(self, ci_id: str = None) -> List[Dict[str, Any]]:
        """
        Get active alerts, optionally filtered by CI
        Args:
            ci_id: Optional CI ID to filter alerts
        Returns:
            List of active alerts
        """
        if ci_id:
            return [alert for alert in self._alerts 
                    if alert["status"] == "active" and alert["ci_id"] == ci_id]
        return [alert for alert in self._alerts if alert["status"] == "active"]

    def get_alert_by_id(self, alert_id: str) -> Dict[str, Any]:
        """Get specific alert by ID"""
        for alert in self._alerts:
            if alert["id"] == alert_id:
                return alert
        return None

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        for alert in self._alerts:
            if alert["id"] == alert_id:
                alert["status"] = "acknowledged"
                alert["acknowledged_at"] = datetime.now()
                return True
        return False

    def get_alert_history(self, ci_id: str = None, 
                         time_range: timedelta = timedelta(days=1)) -> List[Dict[str, Any]]:
        """
        Get alert history for specified time range
        Args:
            ci_id: Optional CI ID to filter alerts
            time_range: Time range to look back (default 1 day)
        Returns:
            List of historical alerts
        """
        now = datetime.now()
        cutoff = now - time_range
        
        alerts = self._alerts
        if ci_id:
            alerts = [alert for alert in alerts if alert["ci_id"] == ci_id]
            
        return [alert for alert in alerts 
                if alert["timestamp"] >= cutoff]

    def get_alert_stats(self) -> Dict[str, int]:
        """Get alert statistics"""
        return {
            "total": len(self._alerts),
            "active": len([a for a in self._alerts if a["status"] == "active"]),
            "critical": len([a for a in self._alerts if a["severity"] == "critical"]),
            "warning": len([a for a in self._alerts if a["severity"] == "warning"]),
            "info": len([a for a in self._alerts if a["severity"] == "info"])
        } 