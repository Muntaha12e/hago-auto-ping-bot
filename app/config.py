import os
from dataclasses import dataclass, field
from typing import Any, Dict


def get_env(key: str, default: Any = None) -> str:
    """Get environment variable with optional default"""
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} is required")
    return str(value)


def get_env_int(key: str, default: int) -> int:
    """Get environment variable as integer"""
    value = os.getenv(key, str(default))
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Environment variable {key} must be an integer, got: {value}")


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get environment variable as boolean"""
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")


@dataclass
class AppSettings:
    # Core Configuration
    ping_interval: int = field(default_factory=lambda: get_env_int("PING_INTERVAL", 30))
    url: str = field(default_factory=lambda: get_env("HAGO_URL", "https://httpbin.org/post"))
    room_id: str = field(default_factory=lambda: get_env("HAGO_ROOM_ID", "demo-room"))
    
    # Retry Configuration
    max_retries: int = field(default_factory=lambda: get_env_int("MAX_RETRIES", 3))
    backoff_factor: float = field(default_factory=lambda: float(os.getenv("BACKOFF_FACTOR", "2.0")))
    
    # Debug & Logging
    debug: bool = field(default_factory=lambda: get_env_bool("DEBUG", False))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    # Timeout
    timeout: int = field(default_factory=lambda: get_env_int("TIMEOUT", 10))
    
    # Headers
    headers: Dict[str, str] = field(
        default_factory=lambda: {
            "Content-Type": "application/json",
            "User-Agent": "HagoAutoPingBot/0.1",
            "Authorization": os.getenv("HAGO_AUTH_TOKEN", ""),
        }
    )
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.ping_interval <= 0:
            raise ValueError(f"PING_INTERVAL must be > 0, got: {self.ping_interval}")
        if self.max_retries < 0:
            raise ValueError(f"MAX_RETRIES must be >= 0, got: {self.max_retries}")
        if self.backoff_factor <= 0:
            raise ValueError(f"BACKOFF_FACTOR must be > 0, got: {self.backoff_factor}")
        if self.timeout <= 0:
            raise ValueError(f"TIMEOUT must be > 0, got: {self.timeout}")


# Load settings from environment variables
settings = AppSettings()
