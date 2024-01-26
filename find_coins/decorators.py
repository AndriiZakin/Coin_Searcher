import time
import logging

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Function {func.__name__} took {elapsed_time} seconds to run.")
        return result
    return wrapper