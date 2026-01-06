import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union
from utils.file_system import FileSystem


def setup_logging(
    logger_name: str,
    level: str = "INFO",
    log_file: Optional[Union[str, Path]] = None,
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    enable_console: bool = True,
    prevent_duplicates: bool = True
) -> logging.Logger:
    """Configures a standard logger with rotation and Airflow safety checks.

    This function initializes a logger with specific handlers. It detects if
    it is running within the Airflow Scheduler to prevent unnecessary file
    creation during DAG parsing.

    Args:
        logger_name: The unique name for the logger (e.g., __name__).
        level: The logging level as a string (e.g., "INFO", "DEBUG").
            Defaults to "INFO".
        log_file: The full path to the log file. If None, file logging
            is disabled. If the scheduler is detected, this is ignored.
        max_file_size: The maximum size of the log file in bytes before
            rotation. Defaults to 10MB.
        backup_count: The number of backup log files to keep. Defaults to 5.
        enable_console: If True, adds a StreamHandler to output to stdout.
            Defaults to True.
        prevent_duplicates: If True, sets propagate=False to avoid duplicate
            logs in the Airflow UI. Defaults to True.

    Returns:
        logging.Logger: A configured Python logger instance.
    """
    try:
        log_level_code = getattr(logging, level.upper())
    except AttributeError:
        print(f"Invalid log level '{level}'. Defaulting to INFO.")
        log_level_code = logging.INFO

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level_code)

    if logger.handlers:
        return logger

    if prevent_duplicates:
        logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level_code)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if log_file:
        log_dir = FileSystem._normalize(log_file).parent
        FileSystem.create_directory(log_dir)
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level_code)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
