import asyncio
import functools
import logging
import time

from logninja import logger as logninja_logger


def log_execution(logger: logging.Logger = logninja_logger):
    """
    Decorator to log the execution time of a function or coroutine.

    Args:
        logger (logging.Logger): The logger to be used.

    Returns:
        Callable: The decorator.
    """

    def decorator(func):
        def log_start(*args, **kwargs):
            params = {"args": list(args), "kwargs": kwargs}
            logger.info(
                f"Starting execution of function {func.__qualname__}",
                extra={"params": params},
            )

        def log_end(end: float, start: float):
            logger.info(f"{func.__qualname__} executed in {end - start:.4f} seconds")

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            log_start(*args, **kwargs)

            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            log_end(end, start)
            return result

        async def async_wrapper(*args, **kwargs):
            log_start(*args, **kwargs)

            start = time.time()
            result = await func(*args, **kwargs)
            end = time.time()

            log_end(end, start)
            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
