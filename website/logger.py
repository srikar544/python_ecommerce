"""
logger.py
---------
Central logging configuration.
"""

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    """
    Configure rotating file logs.
    """

    if not os.path.exists("logs"):
        os.mkdir("logs")

        handler= RotatingFileHandler(
           "logs/app.log",
           maxBytes=10240,
           backupCount=10
        ) 

        formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
         )

        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)

        app.logger.info("Application started")
        