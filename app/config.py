import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default: Any = None) -> str:
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable {key} is required")
    return str(value)


def get_env_int(key: str, default: int) -> int:
    value = os.getenv(key, str(default))
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Environment variable {key} must be an integer, got: {value}") from exc


def get_env_bool(key: str, default: bool = False) -> bool:
    value = os.getenv(key, str(default)).lower()
    return value in ("true", "1", "yes", "on")


@dataclass
class AppSettings:
    ping_interval: int = field(default_factory=lambda: get_env_int("PING_INTERVAL", 30))
    url: str = field(default_factory=lambda: get_env("HAGO_URL", "https://httpbin.org/post"))
    room_id: str = field(default_factory=lambda: get_env("HAGO_ROOM_ID", "demo-room"))
    room_token: str = field(default_factory=lambda: os.getenv("HAGO_ROOM_TOKEN", ""))
    user_id: str = field(default_factory=lambda: os.getenv("HAGO_USER_ID", ""))
    invite_id: str = field(default_factory=lambda: os.getenv("HAGO_INVITE_ID", ""))
    owner_id: str = field(default_factory=lambda: os.getenv("HAGO_OWNER_ID", ""))
    max_retries: int = field(default_factory=lambda: get_env_int("MAX_RETRIES", 3))
    backoff_factor: float = field(default_factory=lambda: float(os.getenv("BACKOFF_FACTOR", "2.0")))
    debug: bool = field(default_factory=lambda: get_env_bool("DEBUG", False))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    timeout: int = field(default_factory=lambda: get_env_int("TIMEOUT", 10))
    health_host: str = field(default_factory=lambda: os.getenv("HEALTH_HOST", "0.0.0.0"))
    health_port: int = field(default_factory=lambda: get_env_int("HEALTH_PORT", 8080))
    headers: Dict[str, str] = field(default_factory=lambda: {
        "Content-Type": "application/json",
        "User-Agent": "HagoAutoPingBot/0.1",
        "Authorization": os.getenv("HAGO_AUTH_TOKEN", ""),
    })

    def __post_init__(self) -> None:
        if self.ping_interval <= 0:
            raise ValueError(f"PING_INTERVAL must be > 0, got: {self.ping_interval}")
        if self.max_retries < 1:
            raise ValueError(f"MAX_RETRIES must be >= 1, got: {self.max_retries}")
        if self.backoff_factor <= 0:
            raise ValueError(f"BACKOFF_FACTOR must be > 0, got: {self.backoff_factor}")
        if self.timeout <= 0:
            raise ValueError(f"TIMEOUT must be > 0, got: {self.timeout}")
        if not 1 <= self.health_port <= 65535:
            raise ValueError(f"HEALTH_PORT must be between 1 and 65535, got: {self.health_port}")


settings = AppSettings()
