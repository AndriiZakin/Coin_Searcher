import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    # Create a custom logger
    logger = logging.getLogger('coin_searcher')

    # Check if the logger has handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevent the logger from propagating messages to the root logger

        # Create handlers
        c_handler = logging.StreamHandler()  # Console handler

        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Delete error log file from previous run
        if os.path.exists('logs/coin_searcher_info.log'):
            os.remove('logs/coin_searcher_info.log')

        # File handler for info with a maximum file size of 1MB
        f_handler_info = RotatingFileHandler('logs/coin_searcher_info.log', maxBytes=1*1024*1024, backupCount=1)
        # File handler for errors with no size limit
        f_handler_error = logging.FileHandler('logs/coin_searcher_error.log')
        
        c_handler.setLevel(logging.INFO)  # Set level for console handler
        f_handler_info.setLevel(logging.INFO)  # Set level for info file handler
        f_handler_error.setLevel(logging.ERROR)  # Set level for error file handler

        # Create formatters and add them to handlers
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        c_handler.setFormatter(format)
        f_handler_info.setFormatter(format)
        f_handler_error.setFormatter(format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler_info)
        logger.addHandler(f_handler_error)

    return logger