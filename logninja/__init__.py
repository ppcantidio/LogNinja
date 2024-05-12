import logging
from contextvars import ContextVar
from typing import List

from logninja.contextvars_filter import ContextVarsFilter
from logninja.json_formatter import JSONFormatter
from logninja.uvicorn_logger_name_filter import UvicornLoggerNameFilter


def setup_logging(
    level: int = logging.INFO,
    fmt: logging.Formatter = JSONFormatter(),
    contextvars: List[ContextVar] = [],
) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=fmt)

    root_logger = logging.getLogger("root")

    root_logger.setLevel(level)

    root_logger.addHandler(stream_handler)

    root_logger.addFilter(UvicornLoggerNameFilter())
    root_logger.addFilter(ContextVarsFilter(contextvars=contextvars))
