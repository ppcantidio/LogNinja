import copy
import json
import logging
from operator import is_
from typing import Union

from logninja.console_interface import ConsoleInterface
from logninja.ninja_console import NinjaConsole
from logninja.ninja_formatter import NinjaFormatter
from logninja.ninja_json_formatter import NinjaJsonFormatter


class NinjaHandler(logging.StreamHandler):
    def __init__(
        self,
        formatter: Union[NinjaJsonFormatter, NinjaFormatter],
        console: ConsoleInterface = NinjaConsole(),
    ):
        super().__init__()
        if not isinstance(formatter, (NinjaJsonFormatter, NinjaFormatter)):
            raise ValueError("Invalid formatter")

        self.console = console
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        formatted_message = self.format(record)
        if self.is_json(formatted_message):
            self.console.print_json(formatted_message)
        else:
            self.console.print(formatted_message)
        self.flush()

    def is_json(self, message: str) -> bool:
        try:
            message_copy = copy.deepcopy(message)
            json.loads(message_copy)
            return True
        except Exception:
            return False
