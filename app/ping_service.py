import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

from app.config import settings
from app.logger import setup_logger

logger = setup_logger("ping_service")


class PingService:
    def __init__(self, url: Optional[str] = None, interval: Optional[int] = None, max_retries: Optional[int] = None, backoff_factor: Optional[float] = None):
        self.url = url or settings.url
        self.interval = interval or settings.ping_interval
        self.running = True
        self.max_retries = max_retries if max_retries is not None else settings.max_retries
        self.backoff_factor = backoff_factor if backoff_factor is not None else settings.backoff_factor
        self.session = requests.Session()
        self.started_at = time.time()
        self.stats = {"total_pings": 0, "successful_pings": 0, "failed_pings": 0}

    def build_payload(self, event: str = "heartbeat") -> Dict[str, Any]:
        return {"event": event, "status": "alive", "room_id": settings.room_id, "timestamp": datetime.now(timezone.utc).isoformat(), "debug": settings.debug}

    def send_ping_with_retry(self) -> bool:
        payload = self.build_payload()
        self.stats["total_pings"] += 1
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info("Sending ping to %s (attempt %d/%d)", self.url, attempt, self.max_retries)
                response = self.session.post(self.url, json=payload, headers=settings.headers, timeout=settings.timeout)
                response.raise_for_status()
                self.stats["successful_pings"] += 1
                logger.info("Ping success: %s", response.status_code)
                return True
            except requests.RequestException as exc:
                logger.warning("Ping attempt %d failed: %s", attempt, exc)
                if attempt < self.max_retries:
                    time.sleep(self.backoff_factor ** (attempt - 1))
        self.stats["failed_pings"] += 1
        logger.error("All retries exhausted for this ping cycle")
        return False

    def send_ping(self) -> bool:
        return self.send_ping_with_retry()

    def get_stats(self) -> Dict[str, Any]:
        total = self.stats["total_pings"]
        success_rate = self.stats["successful_pings"] / total * 100 if total else 0
        return {**self.stats, "success_rate": f"{success_rate:.1f}%", "uptime_seconds": int(time.time() - self.started_at)}

    def run(self) -> None:
        logger.info("Ping service started")
        try:
            while self.running:
                try:
                    self.send_ping_with_retry()
                except Exception as exc:  # pragma: no cover
                    logger.exception("Unexpected error in ping loop: %s", exc)
                time.sleep(self.interval)
        finally:
            self.session.close()

    def stop(self) -> None:
        self.running = False
        logger.info("Ping service stopped; final stats: %s", self.get_stats())
