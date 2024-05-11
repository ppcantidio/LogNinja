import logging
from contextvars import ContextVar

from loggersetup.json_formatter import JSONFormatter
from loggersetup.uvicorn_logger_name_filter import UvicornLoggerNameFilter


def setup_logging(
    level: int = logging.INFO,
    fmt: logging.Formatter = JSONFormatter(),
    global_key: ContextVar = None,
) -> None:
    if isinstance(fmt, JSONFormatter):
        fmt.set_contextvar(global_key)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=fmt)

    root_logger = logging.getLogger("root")
    root_logger.setLevel(level)
    root_logger.addHandler(stream_handler)
    root_logger.addFilter(UvicornLoggerNameFilter())
