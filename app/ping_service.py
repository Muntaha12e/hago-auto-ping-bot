import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

from app.config import settings
from app.logger import setup_logger

logger = setup_logger("ping_service")


class PingService:
    def __init__(self, url: Optional[str] = None, interval: Optional[int] = None):
        self.url = url or settings.url
        self.interval = interval or settings.ping_interval
        self.running = True

    def build_payload(self, event: str = "heartbeat") -> Dict[str, Any]:
        return {
            "event": event,
            "status": "alive",
            "room_id": settings.room_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "debug": settings.debug,
        }

    def send_ping(self) -> bool:
        payload = self.build_payload()
        logger.info("Sending ping to %s", self.url)

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=settings.headers,
                timeout=settings.timeout,
            )
            response.raise_for_status()
            logger.info("Ping success: %s", response.status_code)
            return True
        except requests.RequestException as exc:
            logger.error("Ping failed: %s", exc)
            return False

    def run(self) -> None:
        logger.info("Ping service started")
        while self.running:
            try:
                self.send_ping()
            except Exception as exc:  # pragma: no cover - safety guard
                logger.exception("Unexpected error in ping loop: %s", exc)
            time.sleep(self.interval)

    def stop(self) -> None:
        self.running = False
        logger.info("Ping service stopped")
