from app.config import settings
from app.logger import setup_logger
from app.ping_service import PingService

logger = setup_logger("main")


def main() -> None:
    logger.info("Starting Hago Auto Ping Bot (educational demo)")
    logger.info("URL: %s", settings.url)
    logger.info("Ping interval: %s seconds", settings.ping_interval)

    service = PingService()
    try:
        service.run()
    except KeyboardInterrupt:
        logger.info("Received stop signal")
        service.stop()


if __name__ == "__main__":
    main()
