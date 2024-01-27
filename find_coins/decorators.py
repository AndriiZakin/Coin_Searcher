import time
from main_logger import setup_logger
from functools import wraps
import random

logger = setup_logger()

def timer_decorator(func):
    """
    A decorator that measures the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Function {func.__name__} took {elapsed_time} seconds to run.")
        return result
    return wrapper

def retry_decorator(max_retries):
    """
    A decorator that retries a function if it fails.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Function {func.__name__} failed with error: {e}. Retrying...")
            return None
        return wrapper
    return decorator

def logging_decorator(func):
    """
    A decorator that logs the input and output of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Function {func.__name__} called with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper