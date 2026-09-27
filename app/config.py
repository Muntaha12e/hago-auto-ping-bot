from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AppSettings:
    ping_interval: int = 30
    url: str = "https://httpbin.org/post"
    room_id: str = "demo-room"
    debug: bool = True
    timeout: int = 10
    headers: Dict[str, str] = field(
        default_factory=lambda: {
            "Content-Type": "application/json",
            "User-Agent": "HagoAutoPingBot/0.1",
        }
    )


settings = AppSettings()
