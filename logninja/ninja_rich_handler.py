import logging
import time
from contextvars import ContextVar
from datetime import datetime
from os import times
from typing import List


class NinjaRichHandler(logging.Handler):
    def __init__(self, extras: List[str] = [], level: int = logging.INFO):
        try:
            from rich import get_console
        except ImportError:
            raise ImportError(
                "Rich is required for rich logging. Please install it using `pip install logninja[rich]`"
            )
        super().__init__(level=level)
        self.extras = extras
        self.console = get_console()

    def emit(self, record: logging.LogRecord):
        message = self._get_message(record)
        time_str = self._format_time(record)
        level_color = self._get_level_color(record.levelno)
        extras = self.get_extras(record)
        extras_str = self._format_extras(extras)
        self.console.print(
            f"[grey7]\[{time_str}][/grey7][orange4]\[{record.name}][/orange4][{level_color}]\[{record.levelname}][/{level_color}]    {message}{extras_str}"
        )

    def _get_level_color(self, level: int):
        if level >= logging.CRITICAL:
            return "bold red"
        if level >= logging.ERROR:
            return "bold red"
        if level >= logging.WARNING:
            return "yellow"
        if level >= logging.INFO:
            return "green"
        if level >= logging.DEBUG:
            return "blue"
        return "white"

    def _format_time(self, record: logging.LogRecord, fmt: str = "%Y-%m-%d %H:%M:%S"):
        timestamp = record.created
        dt_object = datetime.fromtimestamp(timestamp)
        time_str = dt_object.strftime(fmt)
        return time_str

    def get_extras(self, record: logging.LogRecord):
        extras = {}
        for extra in self.extras:
            if hasattr(record, extra):
                extras[extra] = getattr(record, extra)
        return extras

    def _format_extras(self, extras: dict):
        extras_str = "    "
        for key, value in extras.items():
            extras_str += f"[bold italic yellow]\[{key}:[/bold italic yellow] [italic]{value}[/italic][bold italic yellow]][/bold italic yellow]"
        return extras_str

    def _get_message(self, record: logging.LogRecord):
        message = record.getMessage()
        if self.formatter:
            record.message = record.getMessage()
            formatter = self.formatter
            if hasattr(formatter, "usesTime") and formatter.usesTime():
                record.asctime = formatter.formatTime(record, formatter.datefmt)
            message = formatter.formatMessage(record)
        return message
