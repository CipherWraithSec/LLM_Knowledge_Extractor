
import sys
from loguru import logger

__all__ = ["setup_logging", "logger"]


def setup_logging():

    # Clear default handlers for cleaner output.
    logger.remove()

    # Add a custom handler for standard output
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        enqueue=True,
    )
