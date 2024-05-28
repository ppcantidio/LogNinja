import logging
from contextvars import ContextVar
from typing import List

from isort import file

from logninja.configs import LogFileConfig
from logninja.contextvars_filter import ContextVarsFilter
from logninja.json_formatter import JSONFormatter

logger = logging.getLogger("logninja")


def setup_logging(
    level: int = logging.INFO,
    fmt: logging.Formatter = JSONFormatter(),
    contextvars: List[ContextVar] = [],
    log_file_config: LogFileConfig = None,
) -> None:

    root_handler = logging.StreamHandler()
    root_handler.setFormatter(fmt=fmt)
    root_handler.addFilter(ContextVarsFilter(contextvars=contextvars))

    root_logger = logging.getLogger()

    root_logger.setLevel(level)

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

    logger.info("Logging setup complete")
