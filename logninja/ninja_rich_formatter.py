import logging
import re
from typing import Any, List, Union

from rich.text import Text

from logninja.options import All, Only
from logninja.utils import (
    format_extras,
    format_path,
    format_time,
    get_extras,
    get_level_name,
    get_message,
)

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


class NinjaRichFormatter(logging.Formatter):
    def __init__(
        self,
        extras: Union[All, Only, None] = None,
        max_message_length: int = 60,
        time_format: str = "%Y-%m-%d %H:%M:%S",
    ):
        super().__init__()
        self.extras = extras
        self.max_message_length = max_message_length
        self.time_format = time_format

    def format(self, record: logging.LogRecord) -> str:
        message = get_message(record, self.max_message_length)
        highlited_message = self._highlight_msg(message)

        time_text = self._style_time(record)
        level_text = self._style_level(record)
        extras_markup = self._style_extras(record)
        path_text = self._style_path(record)
        logger_name_text = Text(f"[{record.name}]", style="orange4")

        markup = self._to_markup(
            time_text,
            level_text,
            highlited_message,
            logger_name_text,
            path_text,
            extras_markup,
        )
        return markup

    def _to_markup(self, *objects: Any) -> str:
        markup = ""
        for obj in objects:
            if isinstance(obj, str):
                markup += " " + obj
            else:
                markup += " " + obj.markup
        return markup

    def _style_path(self, record: logging.LogRecord) -> Text:
        path = format_path(record)
        path_text = Text(path, style="dim u")
        return path_text

    def _style_level(self, record: logging.LogRecord) -> Text:
        level_name = get_level_name(record)
        level_color = self._get_level_color(record.levelno)
        level_text = Text(level_name, style=level_color)
        return level_text

    def _get_level_color(self, levelno: int) -> str:
        colors = {
            logging.CRITICAL: "bold red",
            logging.ERROR: "bold red",
            logging.WARNING: "yellow",
            logging.INFO: "green",
            logging.DEBUG: "blue",
        }
        return colors.get(levelno, "white")

    def _style_time(self, record: logging.LogRecord) -> Text:
        formatted_time = format_time(record, fmt=self.time_format)
        level_text = Text(formatted_time, style="dim")
        return level_text

    def _style_extras(self, record: logging.LogRecord) -> str:
        extras = get_extras(record, extras=self.extras)
        formatted_extras = format_extras(extras)
        formatted_extras = formatted_extras.replace("[", "\[")
        result = re.sub(r"(?<=\=)([\w-]+)", r"[blue]\g<0>[/blue]", formatted_extras)
        result = re.sub(r"([\w-]+)(?=\=)", r"[yellow]\g<0>[/yellow]", result)
        return result

    def _highlight_msg(self, message: str) -> str:
        message = self._highlight_http_status_codes(message)
        message = self._highlight_http_methods(message)
        return message

    def _highlight_http_methods(self, message: str) -> str:
        for method in HTTP_METHODS:
            if method in message:
                message = message.replace(method, f"[bold]{method}[/bold]")
        return message

    def _highlight_http_status_codes(self, message: str) -> str:
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
                message = message.replace(
                    match, f"[bold {color}]{match}[/bold {color}]"
                )
        return message
