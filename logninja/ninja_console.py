import sys

from logninja.console_interface import ConsoleInterface


class NinjaConsole(ConsoleInterface):
    terminator = "\n"

    def __init__(self) -> None:
        self.stream = sys.stderr

    def print(self, message: str):
        try:
            stream = self.stream
            stream.write(message + self.terminator)
        except RecursionError:
            raise

    def print_json(self, message: str):
        try:
            stream = self.stream
            stream.write(message + self.terminator)
        except RecursionError:
            raise
