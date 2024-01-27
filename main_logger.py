import logging

def setup_logger():
    # Create a custom logger
    logger = logging.getLogger('coin_searcher')

    # Check if the logger has handlers
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevent the logger from propagating messages to the root logger

        # Create handlers
        c_handler = logging.StreamHandler()  # Console handler
        f_handler = logging.FileHandler('coin_searcher.log')  # File handler
        c_handler.setLevel(logging.INFO)  # Set level for console handler
        f_handler.setLevel(logging.INFO)  # Set level for file handler

        # Create formatters and add them to handlers
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        c_handler.setFormatter(format)
        f_handler.setFormatter(format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger