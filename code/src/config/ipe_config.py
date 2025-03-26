from typing import Dict, Any
from pydantic import BaseModel

class IPEConfig(BaseModel):
    """Configuration for the IPE agent."""
    
    # LLM settings
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # Process execution settings
    max_retries: int = 3
    retry_delay: int = 5  # seconds
    timeout: int = 300    # seconds
    
    # Workflow settings
    max_concurrent_steps: int = 5
    allow_parallel_execution: bool = True
    
    # Knowledge base settings
    max_kb_entries: int = 1000
    kb_retention_period: int = 86400  # 24 hours in seconds
    
    # Logging settings
    log_level: str = "INFO"
    enable_telemetry: bool = True
    
    # Security settings
    require_auth: bool = True
    allowed_roles: list = ["admin", "support", "viewer"]
    
    # Custom executor settings
    executor_configs: Dict[str, Any] = {
        "api": {
            "max_retries": 3,
            "timeout": 30,
            "verify_ssl": True
        },
        "data_processing": {
            "max_batch_size": 1000,
            "enable_caching": True,
            "cache_ttl": 3600
        }
    }
    
    @classmethod
    def get_default(cls) -> "IPEConfig":
        """Get the default configuration."""
        return cls() 