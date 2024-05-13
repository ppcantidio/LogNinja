import logging
from contextvars import ContextVar
from typing import List

from logninja.contextvars_filter import ContextVarsFilter
from logninja.json_formatter import JSONFormatter

logger = logging.getLogger("logninja")


def setup_logging(
    level: int = logging.INFO,
    fmt: logging.Formatter = JSONFormatter(),
    contextvars: List[ContextVar] = [],
) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=fmt)
    stream_handler.addFilter(ContextVarsFilter(contextvars=contextvars))

    root_logger = logging.getLogger()

    root_logger.setLevel(level)

    root_logger.addHandler(stream_handler)

    logger.info("Logging setup complete")
