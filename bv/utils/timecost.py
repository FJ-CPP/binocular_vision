import time
import logging


def timecost(func):
  """ Decorator to log the time cost of a function
  """
  def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    logging.info(f"{func.__name__} takes {end - start:.3f} seconds")
    return result

  return wrapper
