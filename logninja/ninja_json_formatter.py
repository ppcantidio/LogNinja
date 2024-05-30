import datetime as dt
import json
import logging
from typing import Union

from logninja.options import All, Only
from logninja.traceback import format_exception
from logninja.utils import get_extras

FMT_KEYS = {
    "level": "levelname",
    "message": "message",
    "timestamp": "timestamp",
    "logger": "name",
    "module": "module",
    "function": "funcName",
    "line": "lineno",
    "thread_name": "threadName",
}


class NinjaJsonFormatter(logging.Formatter):
    def __init__(self, extras: Union[All, Only, None] = All):
        super().__init__()
        self.extras = extras

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = format_exception(exc_info=record.exc_info)

        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in FMT_KEYS.items()
        }
        message.update(always_fields)

        extras = get_extras(record=record, extras=self.extras)
        for key, value in extras.items():
            message[key] = value

        return message
