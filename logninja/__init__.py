import logging
from contextvars import ContextVar
from typing import List

from logninja.configs import LogConsoleConfig, LogConsoleType, LogFileConfig
from logninja.console_formatter import ConsoleFormatter
from logninja.contextvars_filter import ContextVarsFilter
from logninja.json_formatter import JSONFormatter
from logninja.ninja_rich_handler import NinjaRichHandler

logger = logging.getLogger("logninja")


def setup_logging(
    level: int = logging.INFO,
    fmt: logging.Formatter = JSONFormatter(),
    contextvars: List[ContextVar] = [],
    log_file_config: LogFileConfig = None,
    log_console_config: LogConsoleConfig = LogConsoleConfig(),
) -> None:
    root_handler = get_root_handler(log_console_config=log_console_config)
    root_handler.addFilter(ContextVarsFilter(contextvars=contextvars))

    root_logger = logging.getLogger()
    root_logger.setLevel(log_console_config.level)
    root_logger.addHandler(root_handler)

    if log_file_config:
        if log_file_config.clear_file_on_setup:
            with open(log_file_config.filename, "w") as f:
                f.write("")
        file_handler = logging.FileHandler(log_file_config.filename)
        file_handler.setFormatter(fmt=log_file_config.fmt)
        file_handler.addFilter(ContextVarsFilter(contextvars=contextvars))
        file_handler.setLevel(log_file_config.level)
        root_logger.addHandler(file_handler)

    logger.info("Logging setup complete", extra=dict(users="adfdfs"))


def get_root_handler(log_console_config: LogConsoleConfig):
    log_console_type = log_console_config.log_console_type
    if log_console_type == LogConsoleType.SIMPLE:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(fmt=ConsoleFormatter)
        return stream_handler
    if log_console_type == LogConsoleType.RICH:
        ninja_rich_handler = NinjaRichHandler(extras=log_console_config.extra_vars)
        ninja_rich_handler.setFormatter(logging.Formatter(fmt="%(message)s"))
        return ninja_rich_handler
    if log_console_type == LogConsoleType.JSON:
        json_handler = logging.StreamHandler()
        json_handler.setFormatter(fmt=JSONFormatter())
        return json_handler
    raise ValueError("Invalid log_console_type")
