from contextvars import ContextVar
from dataclasses import dataclass
from typing import List, Literal, Optional, Union

from logninja.ninja_console import NinjaConsole
from logninja.ninja_formatter import NinjaFormatter
from logninja.ninja_json_formatter import NinjaJsonFormatter

CLASSES = {
    "NinjaConsole": NinjaConsole,
    "NinjaJsonFormatter": NinjaJsonFormatter,
    "NinjaFormatter": NinjaFormatter,
}

LOG_LEVELS = {
    0: "NOTSET",
    10: "DEBUG",
    20: "INFO",
    30: "WARNING",
    40: "ERROR",
    50: "CRITICAL",
}

try:
    from logninja.ninja_rich_console import NinjaRichConsole
except:
    pass
else:
    CLASSES["NinjaRichConsole"] = NinjaRichConsole


@dataclass
class GeneralConfig:
    LOG_CONSOLE_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_CONSOLE_FMT: Literal["NinjaJsonFormatter", "NinjaFormatter"] = (
        "NinjaJsonFormatter"
    )
    LOG_CONSOLE_PRINT_EXCEPTION: bool = True
    LOG_CONSOLE_SYS_EXCEPTHOOK: bool = False
    LOG_CONSOLE_EXTRAS: Union[List[str], Literal["All"]] = "All"
    LOG_CONSOLE_MAX_MESSAGE_LENGTH: int = 40
    LOG_CONSOLE: Literal["NinjaConsole", "NinjaRichConsole"] = "NinjaConsole"

    LOG_FILE_FILENAME: str = "logs.jsonl"
    LOG_FILE_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "ERROR"
    LOG_FILE_FMT: Literal["NinjaJsonFormatter", "NinjaFormatter"] = "NinjaJsonFormatter"
    LOG_FILE_CLEAR_FILE_ON_SETUP: bool = True

    def get_console_level(self) -> int:
        return LOG_LEVELS.get(self.LOG_CONSOLE_LEVEL)

    def get_file_level(self) -> int:
        return LOG_LEVELS.get(self.LOG_FILE_LEVEL)


def setup_logging_by_dynaconf(
    settings: Dynaconf,
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
