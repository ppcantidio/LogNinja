import logging
from typing import Union

from logninja.options import All, Only
from logninja.utils import (
    format_extras,
    format_path,
    format_time,
    get_extras,
    get_level_name,
    get_message,
)


class NinjaFormatter(logging.Formatter):
    def __init__(
        self, extras: Union[All, Only, None] = None, max_message_length: int | None = 60
    ):
        super().__init__()
        self.extras = extras
        self.max_message_length = max_message_length

    def format(self, record: logging.LogRecord) -> str:
        message = get_message(record, self.max_message_length)

        message_time = format_time(record)
        message_level = get_level_name(record)
        filepath = format_path(record)
        extras = get_extras(record=record, extras=self.extras)
        formatted_extras = format_extras(extras)

        structured_message = (
            f"{message_time}{message_level} {message} ({record.name}) {filepath}"
            + formatted_extras
        )

        return structured_message
