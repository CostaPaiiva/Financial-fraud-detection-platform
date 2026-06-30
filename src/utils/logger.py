import logging
import os
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """
    Cria um logger simples para registrar eventos do pipeline.

    Os logs são exibidos no terminal e também salvos na pasta logs/.
    """
    # Ensure the 'logs' directory exists. If not, create it.
    os.makedirs("logs", exist_ok=True)

    # Get a logger instance with the specified name.
    logger = logging.getLogger(name)
    # Set the logging level to INFO, meaning it will process INFO, WARNING, ERROR, and CRITICAL messages.
    logger.setLevel(logging.INFO)

    # Prevent adding duplicate handlers if the logger already has them.
    if logger.handlers:
        return logger

    # Generate a log filename based on the current date, ensuring a new log file each day.
    log_filename = datetime.now().strftime("logs/pipeline_%Y_%m_%d.log")

    # Define the format for log messages.
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Create a console handler to output log messages to the terminal.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # Set console handler level to INFO.
    console_handler.setFormatter(formatter) # Apply the defined format.

    # Create a file handler to write log messages to a file.
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.INFO) # Set file handler level to INFO.
    file_handler.setFormatter(formatter) # Apply the defined format.

    # Add both handlers to the logger.
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger