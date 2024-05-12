import logging
from contextvars import ContextVar
from typing import List


class ContextVarsFilter(logging.Filter):
    def __init__(self, name: str = "", contextvars: List[ContextVar] = []) -> None:
        self.contextvars = contextvars
        super().__init__(name)

    def filter(self, record: logging.LogRecord) -> bool:
        for contextvar in self.contextvars:
            setattr(record, contextvar.name, contextvar.get())
        return True
