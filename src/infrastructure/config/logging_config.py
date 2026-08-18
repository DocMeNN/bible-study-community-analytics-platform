# infrastructure/config/logging_config.py

"""
Logging Configuration

Purpose:
    Provides centralized logging configuration for the OYBS Attendance
    Dashboard application.

Responsibilities:
    - Configure application-wide logging.
    - Create log directory if it does not exist.
    - Configure console and file handlers.
    - Expose a single setup function for application startup.

Usage:
    from src.infrastructure.config.logging_config import configure_logging

    configure_logging()

    import logging
    logger = logging.getLogger(__name__)

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .constants import DEFAULT_LOG_FILE
from .settings import settings


def configure_logging() -> None:
    """
    Configure the application's logging system.

    This function should be called exactly once during application
    startup. Subsequent calls have no effect if logging has already
    been configured.

    Returns:
        None
    """

    root_logger = logging.getLogger()

    # Prevent duplicate handlers when running tests or Streamlit reloads.
    if root_logger.handlers:
        return

    settings.logs_directory.mkdir(parents=True, exist_ok=True)

    log_file: Path = settings.logs_directory / DEFAULT_LOG_FILE

    formatter = logging.Formatter(
        fmt=("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -----------------------------------------------------------------
    # Console Handler
    # -----------------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # -----------------------------------------------------------------
    # Rotating File Handler
    # -----------------------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding=settings.encoding,
    )

    file_handler.setFormatter(formatter)

    # -----------------------------------------------------------------
    # Root Logger
    # -----------------------------------------------------------------

    root_logger.setLevel(settings.log_level)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    root_logger.info("Logging initialized successfully.")


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name:
            Usually __name__.

    Returns:
        logging.Logger:
            Configured logger instance.
    """

    return logging.getLogger(name)
