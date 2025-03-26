from typing import Dict, List, Any
from datetime import datetime
import random

class HealthCheckService:
    def __init__(self):
        self._systems = {
            "web-server-01": {
                "type": "web",
                "services": ["nginx", "application", "monitoring-agent"]
            },
            "app-server-02": {
                "type": "application",
                "services": ["java-app", "redis", "monitoring-agent"]
            },
            "database-01": {
                "type": "database",
                "services": ["postgresql", "backup-service", "monitoring-agent"]
            },
            "cache-server-01": {
                "type": "cache",
                "services": ["redis", "monitoring-agent"]
            }
        }

    def get_available_systems(self) -> List[str]:
        """Get list of available systems"""
        return list(self._systems.keys())

    def run_check(self, system_id: str) -> Dict[str, Any]:
        """
        Run health check on specified system
        In production, this would perform actual system checks
        """
        if system_id not in self._systems:
            raise ValueError(f"System {system_id} not found")

        system = self._systems[system_id]
        checks = {
            "timestamp": datetime.now(),
            "system_id": system_id,
            "system_type": system["type"],
            "status": "healthy",  # or "warning" or "critical"
            "checks": self._perform_system_checks(system),
            "services": self._check_services(system["services"])
        }

        # Determine overall status based on checks
        if any(check["status"] == "critical" for check in checks["checks"]):
            checks["status"] = "critical"
        elif any(check["status"] == "warning" for check in checks["checks"]):
            checks["status"] = "warning"

        return checks

    def _perform_system_checks(self, system: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Perform various system checks"""
        checks = []

        # CPU Check
        cpu_usage = random.uniform(20, 95)
        checks.append({
            "name": "CPU Usage",
            "value": f"{cpu_usage:.1f}%",
            "status": "critical" if cpu_usage > 90 else "warning" if cpu_usage > 75 else "healthy",
            "threshold": "90%"
        })

        # Memory Check
        memory_usage = random.uniform(30, 95)
        checks.append({
            "name": "Memory Usage",
            "value": f"{memory_usage:.1f}%",
            "status": "critical" if memory_usage > 90 else "warning" if memory_usage > 80 else "healthy",
            "threshold": "90%"
        })

        # Disk Check
        disk_usage = random.uniform(40, 95)
        checks.append({
            "name": "Disk Usage",
            "value": f"{disk_usage:.1f}%",
            "status": "critical" if disk_usage > 90 else "warning" if disk_usage > 75 else "healthy",
            "threshold": "90%"
        })

        # Network Check
        network_latency = random.uniform(1, 500)
        checks.append({
            "name": "Network Latency",
            "value": f"{network_latency:.0f}ms",
            "status": "critical" if network_latency > 300 else "warning" if network_latency > 100 else "healthy",
            "threshold": "300ms"
        })

        return checks

    def _check_services(self, services: List[str]) -> List[Dict[str, Any]]:
        """Check status of system services"""
        service_checks = []
        
        for service in services:
            # Simulate service check with random status
            status = random.choices(
                ["running", "warning", "stopped"],
                weights=[0.8, 0.15, 0.05]
            )[0]
            
            service_checks.append({
                "name": service,
                "status": status,
                "uptime": f"{random.randint(1, 30)} days" if status == "running" else "0",
                "memory_usage": f"{random.randint(50, 500)}MB" if status == "running" else "0MB"
            })

        return service_checks

    def get_system_details(self, system_id: str) -> Dict[str, Any]:
        """Get detailed information about a system"""
        if system_id not in self._systems:
            raise ValueError(f"System {system_id} not found")

        system = self._systems[system_id]
        return {
            "id": system_id,
            "type": system["type"],
            "services": system["services"],
            "last_check": self.run_check(system_id)
        } 