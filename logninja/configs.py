import logging
from dataclasses import dataclass, field
from typing import List

from logninja.console_interface import ConsoleInterface
from logninja.ninja_console import NinjaConsole
from logninja.ninja_json_formatter import NinjaJsonFormatter


@dataclass
class LogFileConfig:
    level: int = logging.INFO
    fmt: logging.Formatter = NinjaJsonFormatter()
    filename: str = "logs.jsonl"
    clear_file_on_setup: bool = False


@dataclass
class LogConsoleConfig:
    level: int = logging.INFO
    fmt: logging.Formatter = NinjaJsonFormatter()
    console: ConsoleInterface = NinjaConsole()
    print_exeption: bool = True
    sys_excepthook: bool = False


@dataclass
class RootLoggerConfig:
    level: int = logging.DEBUG
    filters: List[logging.Filter] = field(default_factory=lambda: [])
