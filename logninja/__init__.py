import logging
from contextvars import ContextVar
from typing import List, Mapping

from logninja.configs import LogConsoleConfig, LogFileConfig
from logninja.contextvars_filter import ContextVarsFilter
from logninja.logger import logger
from logninja.ninja_handler import NinjaHandler


def setup_logging(
    contextvars: List[ContextVar] = [],
    log_file_config: LogFileConfig = None,
    log_console_config: LogConsoleConfig = LogConsoleConfig(),
) -> None:
    if log_file_config is None and log_console_config is None:
        raise ValueError(
            "At least one of log_file_config or log_console_config must be provided"
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if log_console_config:
        console_handler = _setup_log_console_handler(log_console_config)
        root_logger.addHandler(console_handler)
        logger.debug("Console logging setup complete")

    if log_file_config:
        file_handler = _setup_log_file_handler(log_file_config)
        root_logger.addHandler(file_handler)
        logger.debug("File logging setup complete")

    root_logger.addFilter(ContextVarsFilter(contextvars=contextvars))

    logger.debug("Logging setup complete", extra=dict(users="adfdfs"))


def setup_logging_by_settings_file(
    settings: Mapping[str, str],
    contextvars: List[ContextVar] = [],
):
    # TODO: Implement this function
    # LOG_CONSOLE_LEVEL = os.getenv("LOG_CONSOLE_LEVEL", "INFO")
    # LOG_CONSOLE_FMT = os.getenv("LOG_CONSOLE_FMT", "NinjaJsonFormatter")
    # LOG_CONSOLE_PRINT_EXCEPTION = os.getenv("LOG_CONSOLE_PRINT_EXCEPTION", "True")
    # LOG_CONSOLE_SYS_EXCEPTHOOK = os.getenv("LOG_CONSOLE_SYS_EXCEPTHOOK", "False")
    # LOG_CONSOLE_EXTRAS = os.getenv("LOG_CONSOLE_EXTRAS", "All")
    # LOG_CONSOLE_MAX_MESSAGE_LENGTH = os.getenv("LOG_CONSOLE_MAX_MESSAGE_LENGTH", "None")

    # LOG_FILE_FILENAME = os.getenv("LOG_FILE_FILENAME", "logs.jsonl")
    # LOG_FILE_LEVEL = os.getenv("LOG_FILE_LEVEL", "ERROR")
    # LOG_FILE_FMT = os.getenv("LOG_FILE_FMT", "NinjaJsonFormatter")
    # LOG_FILE_CLEAR_FILE_ON_SETUP = os.getenv("LOG_FILE_CLEAR_FILE_ON_SETUP", "True")
    pass


def _setup_log_console_handler(
    log_console_config: LogConsoleConfig,
) -> logging.StreamHandler:
    console_handler = NinjaHandler(
        formatter=log_console_config.fmt,
        console=log_console_config.console,
        print_exception=log_console_config.print_exeption,
        sys_excepthook=log_console_config.sys_excepthook,
    )
    console_handler.setLevel(log_console_config.level)
    return console_handler


def _setup_log_file_handler(log_file_config: LogFileConfig) -> logging.FileHandler:
    if log_file_config.clear_file_on_setup:
        with open(log_file_config.filename, "w") as f:
            f.write("")

    file_handler = logging.FileHandler(log_file_config.filename)
    file_handler.setFormatter(fmt=log_file_config.fmt)
    file_handler.setLevel(log_file_config.level)

    return file_handler
