import pandas as pd
import random
from datetime import datetime, timedelta

def generate_incident_data(num_records=100):
    """Generate sample incident data"""
    priorities = ["High", "Medium", "Low"]
    statuses = ["Open", "In Progress", "Resolved", "Closed"]
    categories = ["System", "Network", "Database", "Application", "Security"]
    
    incidents = []
    for i in range(num_records):
        incident = {
            "id": f"INC{str(i+1).zfill(4)}",
            "title": f"Sample Incident {i+1}",
            "description": f"This is a sample incident description for incident {i+1}",
            "priority": random.choice(priorities),
            "status": random.choice(statuses),
            "category": random.choice(categories),
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "updated_at": (datetime.now() - timedelta(days=random.randint(0, 5))).isoformat()
        }
        incidents.append(incident)
    return pd.DataFrame(incidents)

def generate_kb_articles():
    """Generate sample knowledge base articles"""
    articles = [
        {
            "id": "KB001",
            "title": "Common System Issues and Solutions",
            "content": """
            # Common System Issues
            
            ## High CPU Usage
            - Check running processes
            - Review application logs
            - Monitor system resources
            
            ## Memory Issues
            - Check memory leaks
            - Review application memory usage
            - Analyze heap dumps
            """,
            "category": "Troubleshooting",
            "tags": ["system", "cpu", "memory"]
        },
        {
            "id": "KB002",
            "title": "Network Troubleshooting Guide",
            "content": """
            # Network Troubleshooting
            
            ## Connection Issues
            - Check network connectivity
            - Verify DNS settings
            - Test network latency
            
            ## Security Issues
            - Review firewall rules
            - Check security logs
            - Verify access controls
            """,
            "category": "Network",
            "tags": ["network", "connectivity", "security"]
        }
    ]
    return pd.DataFrame(articles)

def generate_telemetry_data(hours=24):
    """Generate sample telemetry data"""
    timestamps = pd.date_range(
        start=datetime.now() - timedelta(hours=hours),
        end=datetime.now(),
        freq='5min'
    )
    
    data = []
    for ts in timestamps:
        data.append({
            "timestamp": ts,
            "cpu_usage": random.uniform(20, 90),
            "memory_usage": random.uniform(30, 85),
            "disk_usage": random.uniform(40, 75),
            "network_latency": random.uniform(10, 200)
        })
    return pd.DataFrame(data) 