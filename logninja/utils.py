import logging
from datetime import datetime
from pathlib import Path
from typing import List, Union

from logninja.options import All, Only

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


def get_message(record: logging.LogRecord, max_len: int | None) -> str:
    message = record.getMessage()
    import json

    try:
        result = json.loads(message)
        if result.get("message"):
            message = result.get("message")
    except Exception:
        pass

    if max_len is None:
        return message

    message_size = len(message)
    if message_size == max_len:
        return message

    if message_size > max_len:
        message = message[:max_len] + "..."
        return message

    if message_size < max_len:
        message = message + " " * (max_len + 3 - message_size)

    return message


def format_path(record: logging.LogRecord) -> str:
    path = Path(record.pathname).name
    result = f"{path}:{record.lineno}"
    return result


def get_all_extras(record: logging.LogRecord) -> dict:
    extras_result = {}
    for key, val in record.__dict__.items():
        if key not in LOG_RECORD_BUILTIN_ATTRS:
            extras_result[key] = val
    return extras_result


def get_only_extras(record: logging.LogRecord, extras: List[str]) -> dict:
    extras_result = {}
    for key in extras:
        if key in record.__dict__:
            extras_result[key] = record.__dict__[key]
    return extras_result


def get_extras(
    record: logging.LogRecord,
    extras: Union[All, Only, None],
) -> dict:
    if extras is None:
        return {}

    if isinstance(extras, All):
        return get_all_extras(record)
    if isinstance(extras, Only):
        return get_only_extras(record, extras.extras)

    raise Exception("Invalid option, use All(),  Only([list of extras]) or None")


def get_level_name(record: logging.LogRecord) -> str:
    levelno = record.levelno
    levels = {
        logging.CRITICAL: "[CRITICAL]",
        logging.ERROR: "[ERROR   ]",
        logging.WARNING: "[WARNING ]",
        logging.INFO: "[INFO    ]",
        logging.DEBUG: "[DEBUG   ]",
    }
    level_name = levels.get(levelno)
    return level_name


def format_time(record: logging.LogRecord, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    timestamp = record.created
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_time = dt_object.strftime(fmt)
    return f"[{formatted_time}]"


def format_extras(extras: dict) -> str:
    text = ""
    if extras:
        last_key = list(extras.keys())[-1]
        for key, value in extras.items():
            key_value = f"{key}={value}"
            text += key_value
            if key != last_key:
                text += ", "
        return f"  [{text}]"

    return text
