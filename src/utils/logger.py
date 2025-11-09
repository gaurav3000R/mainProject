"""Logging configuration using Loguru."""
import sys
from pathlib import Path
from loguru import logger
from src.core.config import settings


def setup_logging():
    """Configure application logging."""
    
    # Remove default handler
    logger.remove()
    
    # Console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # File handler for all logs
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        compression="zip",
    )
    
    # Error file handler
    logger.add(
        log_path / "error_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="90 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    return logger


# Global logger instance
app_logger = setup_logging()
