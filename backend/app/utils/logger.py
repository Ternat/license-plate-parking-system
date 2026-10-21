import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Configure system logger with console and file output.
    Rotate log files to prevent oversized logs.
    """
    logger = logging.getLogger("uk_lpr_parking_system")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "parking_system.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()