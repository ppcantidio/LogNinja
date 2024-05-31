import logging
from dataclasses import dataclass
from typing import Optional

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
