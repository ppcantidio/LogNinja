import sys

from logninja.console_interface import ConsoleInterface


class NinjaConsole(ConsoleInterface):
    terminator = "\n"

    def __init__(self) -> None:
        self.stream = sys.stderr

    def print(self, *objects: str, **kwargs) -> None:
        try:
            stream = self.stream
            final_message = "".join(objects)
            stream.write(final_message + self.terminator)
        except RecursionError:
            raise

    def print_json(self, json: str, *args, **kwargs) -> None:
        self.print(json, *args, **kwargs)
