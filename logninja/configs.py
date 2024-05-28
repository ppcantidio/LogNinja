import logging
from dataclasses import dataclass

from logninja.json_formatter import JSONFormatter


@dataclass
class LogFileConfig:
    filename: str = "logs.jsonl"
    level: int = logging.INFO
    clear_file_on_setup: bool = False
    fmt: logging.Formatter = JSONFormatter()
