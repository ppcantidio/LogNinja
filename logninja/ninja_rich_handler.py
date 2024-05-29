import logging
import re
from datetime import datetime
from os import times
from pathlib import Path
from typing import List

from rich.text import Text

HTTP_METHODS: List[str] = [
    "GET",
    "POST",
    "HEAD",
    "PUT",
    "DELETE",
    "OPTIONS",
    "TRACE",
    "PATCH",
]


def highlight_http_methods(message: str) -> str:
    for method in HTTP_METHODS:
        if method in message:
            message = message.replace(method, f"[bold]{method}[/bold]")
    return message


def highlight_http_status_codes(message: str) -> str:
    status_codes = {
        "1..": "blue",  # Informational
        "2..": "green",  # Success
        "3..": "yellow",  # Redirection
        "4..": "red",  # Client errors
        "5..": "magenta",  # Server errors
    }

    for status_code, color in status_codes.items():
        status_code_pattern = status_code.replace("..", "\d\d")
        pattern = re.compile(rf"\b{status_code_pattern}\b")
        matches = pattern.findall(message)
        for match in matches:
            message = message.replace(match, f"[bold {color}]{match}[/bold {color}]")
    return message


class NinjaRichHandler(logging.Handler):
    def __init__(self, extras: List[str] = [], max_message_length: int = 44):
        try:
            from rich import get_console
        except ImportError:
            raise ImportError(
                "Rich is required for rich logging. Please install it using `pip install logninja[rich]`"
            )
        super().__init__()
        self.extras = extras
        self.max_message_length = max_message_length
        self.console = get_console()

    def emit(self, record: logging.LogRecord):
        message = self._get_message(record)
        time_text = self._format_time(record)
        level_text = self._get_level_text(record.levelno)
        extras = self.get_extras(record)
        extras_text = self._format_extras(extras)
        format_path = self._format_path(record)
        logger_name_style = Text(f"[{record.name}]", style="orange4")
        self.console.print(
            time_text,
            level_text,
            message,
            logger_name_style,
            format_path,
            extras_text,
        )

    def _format_path(self, record: logging.LogRecord):
        path = Path(record.pathname).name
        path_text = Text()
        path_text.append(
            path, style=f"dim link file://{record.pathname}" if record.pathname else ""
        )
        path_text.append(":")
        path_text.append(
            str(record.lineno),
            style=(
                f"dim link file://{record.pathname}#{record.lineno}"
                if record.pathname
                else ""
            ),
        )

        return path_text

    def _get_level_text(self, level: int) -> Text:
        space = " " * 0
        levels = {
            logging.CRITICAL: Text("[CRITICAL]" + space, style="bold red"),
            logging.ERROR: Text("[ERROR   ]" + space, style="bold red"),
            logging.WARNING: Text("[WARNING ]" + space, style="yellow"),
            logging.INFO: Text("[INFO    ]" + space, style="green"),
            logging.DEBUG: Text("[DEBUG   ]" + space, style="blue"),
        }
        level_name = levels.get(level)
        return level_name

    def _format_time(self, record: logging.LogRecord, fmt: str = "%Y-%m-%d %H:%M:%S"):
        timestamp = record.created
        dt_object = datetime.fromtimestamp(timestamp)
        time_str = dt_object.strftime(fmt)
        text = Text(f"[{time_str}]", style="dim")
        return text

    def get_extras(self, record: logging.LogRecord):
        extras = {}
        for extra in self.extras:
            if hasattr(record, extra):
                extras[extra] = getattr(record, extra)
        return extras

    def _format_extras(self, extras: dict):
        if extras:
            text = Text()
            text.append("  [")
            last_key = list(extras.keys())[-1]
            for key, value in extras.items():
                text.append(key, style="yellow")
                text.append("=")
                text.append(str(value), style="blue")
                if key != last_key:
                    text.append(", ")
            text.append("]")
            return text
        return ""

    def _get_message(self, record: logging.LogRecord):
        message = record.getMessage()
        if self.formatter:
            record.message = record.getMessage()
            formatter = self.formatter
            if hasattr(formatter, "usesTime") and formatter.usesTime():
                record.asctime = formatter.formatTime(record, formatter.datefmt)
            message = formatter.formatMessage(record)

        message_size = len(message)
        max_size = self.max_message_length
        if message_size == max_size:
            return message
        if message_size > max_size:
            message = message[:max_size] + "..."
            return message
        if message_size < max_size:
            message = message + " " * (max_size + 3 - message_size)

        message = highlight_http_status_codes(message)
        return highlight_http_methods(message)
