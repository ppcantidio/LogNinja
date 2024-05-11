import datetime as dt
import json
import logging
from contextvars import ContextVar

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


class JSONFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def set_contextvar(self, contextvar: ContextVar):
        self.contextvar = contextvar

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: (
                msg_val
                if (msg_val := always_fields.pop(val, None)) is not None
                else getattr(record, val)
            )
            for key, val in FMT_KEYS.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        if self.contextvar:
            message[self.contextvar.name] = self.contextvar.get()

        return message
