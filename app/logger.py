import logging
import os

from dotenv import load_dotenv

from app.config import settings

# Load .env file jika ada
load_dotenv()


def setup_logger(name: str = "hago_auto_ping") -> logging.Logger:
    """Setup logger dengan level dari environment variable LOG_LEVEL"""
    logger = logging.getLogger(name)
    
    # Parse log level dari settings
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
