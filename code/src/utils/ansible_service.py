import os
import json
from typing import Dict, List, Any
from datetime import datetime
import subprocess
from pathlib import Path

class AnsibleService:
    def __init__(self):
        self.playbooks_dir = Path("ansible/playbooks")
        self.inventory_file = Path("ansible/inventory.yml")
        self._action_history = []
        
        # Initialize with sample playbooks (in production, these would be real Ansible playbooks)
        self._available_playbooks = {
            "health_check": {
                "name": "System Health Check",
                "description": "Run system health diagnostics",
                "playbook": "health_check.yml",
                "params": ["target_host"]
            },
            "restart_service": {
                "name": "Restart Service",
                "description": "Restart a specific service",
                "playbook": "restart_service.yml",
                "params": ["service_name", "target_host"]
            },
            "disk_cleanup": {
                "name": "Disk Cleanup",
                "description": "Clean up temporary files and old logs",
                "playbook": "disk_cleanup.yml",
                "params": ["target_host", "older_than_days"]
            }
        }

    def get_available_playbooks(self) -> List[Dict[str, Any]]:
        """Get list of available playbooks with their details"""
        return [
            {
                "id": playbook_id,
                **playbook_info
            }
            for playbook_id, playbook_info in self._available_playbooks.items()
        ]

    def get_playbook_params(self, playbook_id: str) -> List[str]:
        """Get required parameters for a specific playbook"""
        if playbook_id in self._available_playbooks:
            return self._available_playbooks[playbook_id]["params"]
        return []

    def run_playbook(self, playbook_id: str, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Run an Ansible playbook with provided parameters
        In this example, we'll simulate playbook execution
        """
        if playbook_id not in self._available_playbooks:
            raise ValueError(f"Playbook {playbook_id} not found")

        # Validate required parameters
        required_params = self._available_playbooks[playbook_id]["params"]
        for param in required_params:
            if param not in params:
                raise ValueError(f"Missing required parameter: {param}")

        # Simulate playbook execution
        execution_id = f"exec_{len(self._action_history) + 1}"
        
        # Record the action
        action = {
            "id": execution_id,
            "playbook_id": playbook_id,
            "params": params,
            "timestamp": datetime.now(),
            "status": "success",
            "output": self._simulate_playbook_output(playbook_id, params)
        }
        
        self._action_history.append(action)
        return action

    def get_recent_actions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent automation actions"""
        return sorted(
            self._action_history,
            key=lambda x: x["timestamp"],
            reverse=True
        )[:limit]

    def _simulate_playbook_output(self, playbook_id: str, params: Dict[str, str]) -> Dict[str, Any]:
        """Simulate playbook execution output"""
        if playbook_id == "health_check":
            return {
                "cpu_usage": "32%",
                "memory_usage": "45%",
                "disk_usage": "68%",
                "services_status": "all running",
                "checks_passed": True
            }
        elif playbook_id == "restart_service":
            return {
                "service": params["service_name"],
                "status": "restarted",
                "uptime": "0m",
                "result": "success"
            }
        elif playbook_id == "disk_cleanup":
            return {
                "space_freed": "2.3GB",
                "files_removed": 156,
                "status": "completed"
            }
        return {"status": "completed"}

    def validate_inventory(self, target_host: str) -> bool:
        """Validate if a host exists in inventory"""
        # In production, this would check actual Ansible inventory
        return target_host in ["web-server-01", "app-server-02", "database-01"] 