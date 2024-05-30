import logging
from typing import Union

from logninja.ninja_console import NinjaConsole
from logninja.ninja_formatter import NinjaFormatter
from logninja.ninja_json_formatter import NinjaJsonFormatter
from logninja.ninja_rich_formatter import NinjaRichFormatter


class NinjaHandler(logging.StreamHandler):
    def __init__(
        self, formatter: Union[NinjaJsonFormatter, NinjaRichFormatter, NinjaFormatter]
    ):
        super().__init__()
        if not isinstance(
            formatter, (NinjaJsonFormatter, NinjaRichFormatter, NinjaFormatter)
        ):
            raise ValueError("Invalid formatter")

        self.console = NinjaConsole(stream=self.stream)

        if isinstance(formatter, NinjaRichFormatter):
            try:
                from rich import get_console

                self.console = get_console()
            except ImportError:
                raise ImportError(
                    "Rich is required for rich logging. Please install it using `pip install logninja[rich]`"
                )

        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        formatted_message = self.format(record)
        self.console.print(formatted_message)
        self.flush()
