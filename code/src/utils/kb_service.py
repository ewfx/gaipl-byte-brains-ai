from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import os
from datasets import load_dataset
import random

class KBService:
    def __init__(self):
        # Initialize with sample knowledge base data
        self._articles = self._initialize_articles()
        self._guides = self._initialize_guides()
        self._stack_overflow = self._initialize_stack_overflow()
        self._documentation = self._initialize_documentation()
        
        # Try to load external data
        self._load_external_data()

    def _initialize_articles(self) -> List[Dict[str, Any]]:
        """Initialize sample KB articles"""
        return [
            {
                "id": "KB001",
                "title": "Common System Issues and Solutions",
                "category": "Troubleshooting",
                "content": """
                # Common System Issues and Solutions
                
                ## High CPU Usage
                - Check for resource-intensive processes
                - Review application logs
                - Monitor system metrics
                
                ## Memory Leaks
                - Identify memory-consuming processes
                - Analyze heap dumps
                - Review application memory settings
                """,
                "tags": ["system", "cpu", "memory", "troubleshooting"],
                "last_updated": datetime.now() - timedelta(days=5)
            },
            {
                "id": "KB002",
                "title": "Database Performance Optimization",
                "category": "Best Practices",
                "content": """
                # Database Performance Optimization
                
                ## Index Optimization
                - Review query execution plans
                - Analyze index usage
                - Implement missing indexes
                
                ## Query Tuning
                - Identify slow queries
                - Optimize query structure
                - Use query hints when necessary
                """,
                "tags": ["database", "performance", "optimization"],
                "last_updated": datetime.now() - timedelta(days=2)
            },
            {
                "id": "KB003",
                "title": "Network Security Best Practices",
                "category": "Security",
                "content": """
                # Network Security Best Practices
                
                ## Firewall Configuration
                - Implement proper firewall rules
                - Regular security audits
                - Monitor network traffic
                
                ## Access Control
                - Implement role-based access
                - Regular password rotation
                - Monitor access logs
                """,
                "tags": ["security", "network", "firewall"],
                "last_updated": datetime.now() - timedelta(days=1)
            },
            {
                "id": "KB004",
                "title": "Application Deployment Guide",
                "category": "Deployment",
                "content": """
                # Application Deployment Guide
                
                ## Pre-deployment Checklist
                - Run automated tests
                - Check dependencies
                - Verify configurations
                
                ## Deployment Process
                - Use blue-green deployment
                - Monitor health checks
                - Rollback procedures
                """,
                "tags": ["deployment", "ci-cd", "automation"],
                "last_updated": datetime.now() - timedelta(days=3)
            }
        ]

    def _initialize_guides(self) -> List[Dict[str, Any]]:
        """Initialize sample troubleshooting guides"""
        return [
            {
                "id": "TG001",
                "title": "Resolving High CPU Usage",
                "system": "Linux Servers",
                "problem": "System experiencing sustained high CPU usage",
                "steps": [
                    "Check top processes using 'top' command",
                    "Review system logs in /var/log/",
                    "Monitor CPU usage patterns",
                    "Identify and optimize resource-intensive applications"
                ],
                "verification": "CPU usage should return to normal levels (<70%)",
                "tags": ["cpu", "performance", "linux"],
                "last_updated": datetime.now() - timedelta(days=1)
            },
            {
                "id": "TG002",
                "title": "Database Connection Issues",
                "system": "Database Servers",
                "problem": "Applications unable to connect to database",
                "steps": [
                    "Verify database service status",
                    "Check network connectivity",
                    "Review firewall rules",
                    "Validate credentials"
                ],
                "verification": "Test database connection using client tools",
                "tags": ["database", "connectivity", "troubleshooting"],
                "last_updated": datetime.now() - timedelta(days=2)
            },
            {
                "id": "TG003",
                "title": "Web Server Performance Issues",
                "system": "Web Servers",
                "problem": "Slow response times and high latency",
                "steps": [
                    "Check server resources",
                    "Review application logs",
                    "Analyze network traffic",
                    "Optimize configurations"
                ],
                "verification": "Response times should be under 200ms",
                "tags": ["web", "performance", "optimization"],
                "last_updated": datetime.now() - timedelta(days=3)
            }
        ]

    def _initialize_stack_overflow(self) -> List[Dict[str, Any]]:
        """Initialize sample Stack Overflow posts"""
        return [
            {
                "id": "SO001",
                "title": "How to optimize PostgreSQL query performance?",
                "question": "I have a complex query that's running slowly...",
                "accepted_answer": """
                1. First, analyze the query using EXPLAIN ANALYZE
                2. Check for missing indexes
                3. Review query structure
                """,
                "score": 125,
                "tags": ["postgresql", "performance", "sql"],
                "timestamp": datetime.now() - timedelta(days=30)
            },
            {
                "id": "SO002",
                "title": "Best practices for Docker container security",
                "question": "What are the essential security measures for Docker containers?",
                "accepted_answer": """
                1. Use official base images
                2. Implement least privilege principle
                3. Regular security scanning
                4. Keep images updated
                """,
                "score": 98,
                "tags": ["docker", "security", "containers"],
                "timestamp": datetime.now() - timedelta(days=25)
            },
            {
                "id": "SO003",
                "title": "Monitoring Kubernetes cluster health",
                "question": "What metrics should I monitor in my Kubernetes cluster?",
                "accepted_answer": """
                1. Node health and resources
                2. Pod status and metrics
                3. Service availability
                4. Network performance
                """,
                "score": 156,
                "tags": ["kubernetes", "monitoring", "devops"],
                "timestamp": datetime.now() - timedelta(days=20)
            }
        ]

    def _initialize_documentation(self) -> List[Dict[str, Any]]:
        """Initialize sample documentation"""
        return [
            {
                "id": "DOC001",
                "title": "System Architecture Overview",
                "category": "Architecture",
                "content": """
                # System Architecture
                
                ## Components
                - Web Servers
                - Application Servers
                - Database Servers
                
                ## Network Layout
                - DMZ Configuration
                - Internal Network
                - Backup Systems
                """,
                "last_updated": datetime.now() - timedelta(days=10)
            },
            {
                "id": "DOC002",
                "title": "CI/CD Pipeline Documentation",
                "category": "DevOps",
                "content": """
                # CI/CD Pipeline
                
                ## Build Process
                - Source code compilation
                - Unit testing
                - Integration testing
                
                ## Deployment Process
                - Environment setup
                - Configuration management
                - Release management
                """,
                "last_updated": datetime.now() - timedelta(days=8)
            },
            {
                "id": "DOC003",
                "title": "Security Policies and Procedures",
                "category": "Security",
                "content": """
                # Security Policies
                
                ## Access Control
                - User authentication
                - Role-based access
                - Audit logging
                
                ## Incident Response
                - Detection procedures
                - Response protocols
                - Recovery steps
                """,
                "last_updated": datetime.now() - timedelta(days=5)
            }
        ]

    def _load_external_data(self):
        """Load additional data from external sources"""
        try:
            # Try to load from Hugging Face datasets
            self._load_from_huggingface()
        except Exception as e:
            print(f"Error loading from Hugging Face: {str(e)}")
            
        try:
            # Try to load from local data directory
            self._load_from_local()
        except Exception as e:
            print(f"Error loading from local directory: {str(e)}")

    def _load_from_huggingface(self):
        """Load data from Hugging Face datasets"""
        try:
            # Load Stack Overflow dataset
            stack_overflow_dataset = load_dataset("stack_overflow")
            if stack_overflow_dataset:
                for item in stack_overflow_dataset['train'][:10]:  # Load first 10 items
                    self._stack_overflow.append({
                        "id": f"SO-{len(self._stack_overflow) + 1}",
                        "title": item['title'],
                        "question": item['body'],
                        "accepted_answer": item.get('accepted_answer', ''),
                        "score": item.get('score', 0),
                        "tags": item.get('tags', []),
                        "timestamp": datetime.now() - timedelta(days=random.randint(1, 30))
                    })
        except Exception as e:
            print(f"Error loading Stack Overflow data: {str(e)}")

    def _load_from_local(self):
        """Load data from local data directory"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'kb')
        if not os.path.exists(data_dir):
            return

        # Load articles
        articles_file = os.path.join(data_dir, 'articles.json')
        if os.path.exists(articles_file):
            with open(articles_file, 'r') as f:
                articles = json.load(f)
                self._articles.extend(articles)

        # Load guides
        guides_file = os.path.join(data_dir, 'guides.json')
        if os.path.exists(guides_file):
            with open(guides_file, 'r') as f:
                guides = json.load(f)
                self._guides.extend(guides)

        # Load documentation
        docs_file = os.path.join(data_dir, 'documentation.json')
        if os.path.exists(docs_file):
            with open(docs_file, 'r') as f:
                docs = json.load(f)
                self._documentation.extend(docs)

    def search_articles(self, query: str) -> List[Dict[str, Any]]:
        """Search KB articles"""
        if not query:
            return []
        return [
            article for article in self._articles
            if query.lower() in article['title'].lower() or
               query.lower() in article['content'].lower() or
               any(query.lower() in tag.lower() for tag in article['tags'])
        ]

    def get_recent_articles(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent KB articles"""
        return sorted(
            self._articles,
            key=lambda x: x['last_updated'],
            reverse=True
        )[:limit]

    def search_guides(self, query: str) -> List[Dict[str, Any]]:
        """Search troubleshooting guides"""
        if not query:
            return []
        return [
            guide for guide in self._guides
            if query.lower() in guide['title'].lower() or
               query.lower() in guide['problem'].lower()
        ]

    def get_recent_guides(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent troubleshooting guides"""
        return sorted(
            self._guides,
            key=lambda x: x['last_updated'],
            reverse=True
        )[:limit]

    def search_stack_overflow(self, query: str) -> List[Dict[str, Any]]:
        """Search Stack Overflow posts"""
        if not query:
            return []
        return [
            post for post in self._stack_overflow
            if query.lower() in post['title'].lower() or
               query.lower() in post['question'].lower()
        ]

    def get_top_posts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top-rated Stack Overflow posts"""
        return sorted(
            self._stack_overflow,
            key=lambda x: x['score'],
            reverse=True
        )[:limit]

    def search_documentation(self, query: str) -> List[Dict[str, Any]]:
        """Search documentation"""
        if not query:
            return []
        return [
            doc for doc in self._documentation
            if query.lower() in doc['title'].lower() or
               query.lower() in doc['content'].lower()
        ]

    def get_recent_docs(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent documentation"""
        return sorted(
            self._documentation,
            key=lambda x: x['last_updated'],
            reverse=True
        )[:limit] 