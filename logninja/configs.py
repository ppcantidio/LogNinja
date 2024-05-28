import logging
from dataclasses import dataclass
from enum import Enum
from typing import List

from click.utils import R

from logninja.json_formatter import JSONFormatter


class LogConsoleType(Enum):
    SIMPLE = "simple_console"
    RICH = "rich_console"
    JSON = "json"


@dataclass
class LogFileConfig:
    filename: str = "logs.jsonl"
    level: int = logging.INFO
    clear_file_on_setup: bool = False
    fmt: logging.Formatter = JSONFormatter()


@dataclass
class LogConsoleConfig:
    level: int = logging.INFO
    log_console_type: LogConsoleType = LogConsoleType.SIMPLE
    extra_vars: List[str] = None
