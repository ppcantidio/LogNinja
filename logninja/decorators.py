import asyncio
import functools
import logging
import time

logger = logging.getLogger(__name__)


def log_execution(func):
    """
    Decorator to log the execution time of a function or coroutine.

    Args:
        func (Callable): The function or coroutine to be decorated.

    Returns:
        Callable: The decorated function or coroutine.
    """

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
