import signal

from app.config import settings
from app.health import start_health_server
from app.logger import setup_logger
from app.ping_service import PingService

logger = setup_logger("main")


def main() -> None:
    service = PingService()
    health_server = start_health_server(service.get_stats, settings.health_host, settings.health_port)
    logger.info("Health endpoint: http://%s:%d/health", settings.health_host, settings.health_port)

    def stop_handler(signum: int, frame: object) -> None:
        logger.info("Received stop signal: %s", signum)
        service.stop()
        health_server.shutdown()

    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)
    service.run()


if __name__ == "__main__":
    main()
