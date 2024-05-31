import copy
import json
import logging
import sys
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
        print_exception: bool = True,
        sys_excepthook: bool = False,
    ):
        super().__init__()
        if not isinstance(formatter, (NinjaJsonFormatter, NinjaFormatter)):
            raise ValueError("Invalid formatter")

        self.sys_excepthook = sys_excepthook
        self.print_exception = print_exception
        self.console = console
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        formatted_message = self.format(record)
        if self.is_json(formatted_message):
            self.console.print_json(formatted_message)
        else:
            self.console.print(formatted_message)
        self.flush()

        if record.exc_info and self.print_exception:
            self.console.print_exception(show_locals=True)

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

        if self.sys_excepthook is False:
            sys.excepthook = handle_exception

    def is_json(self, message: str) -> bool:
        try:
            message_copy = copy.deepcopy(message)
            json.loads(message_copy)
            return True
        except Exception:
            return False
