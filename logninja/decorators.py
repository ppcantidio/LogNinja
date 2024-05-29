import asyncio
import functools
import logging
import time

from logninja import logger as logninja_logger


def log_execution(
    logger: logging.Logger = logninja_logger,
    level: int = logging.INFO,
    capture_exception: bool = False,
    raise_exception: bool = False,
):
    """
    Decorator to log the execution time of a function or coroutine.

    Args:
        logger (logging.Logger): The logger to be used.
        level (int): The logging level to be used.
        capture_exception (bool): Whether to capture exceptions. Defaults to False.
        raise_exception (bool): Whether to raise exceptions. Defaults to False.

    Warning:
        If capture_exception is True and raise_exception is False, the exception will be logged but not raised.
        The return value will be the exception object.

    Returns:
        Callable: The decorator.
    """

    def decorator(func):
        if (raise_exception is True) and (capture_exception is False):
            raise ValueError(
                "Cannot raise exception without capturing it, set capture_exception to True"
            )
        levels = {
            logging.CRITICAL: "critical",
            logging.ERROR: "error",
            logging.WARNING: "warning",
            logging.INFO: "info",
            logging.DEBUG: "debug",
        }
        level_attr = levels.get(level, "info")
        logger_with_level = getattr(logger, level_attr)

        def log_start(*args, **kwargs):
            params = {"args": list(args), "kwargs": kwargs}
            logger_with_level(
                f"Starting execution of function {func.__qualname__}",
                extra={"params": params},
            )

        def log_end(end: float, start: float):
            logger_with_level(
                f"{func.__qualname__} executed in {end - start:.4f} seconds"
            )

        def log_exception(exc: Exception):
            logger.exception(
                f"An error occurred while executing {func.__qualname__}",
                exc_info=exc,
            )
            if raise_exception:
                raise exc

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            log_start(*args, **kwargs)

            start = time.time()
            if capture_exception:
                try:
                    result = func(*args, **kwargs)
                except Exception as exc:
                    log_exception(exc)
                    return exc
            else:
                result = func(*args, **kwargs)
            end = time.time()

            log_end(end, start)
            return result

        async def async_wrapper(*args, **kwargs):
            log_start(*args, **kwargs)

            start = time.time()
            if capture_exception:
                try:
                    result = await func(*args, **kwargs)
                except Exception as exc:
                    log_exception(exc)
                    return exc
            else:
                result = await func(*args, **kwargs)
            end = time.time()

            log_end(end, start)
            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
