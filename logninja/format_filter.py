import logging


class FormatFilter(logging.Filter):
    """
    In some cases, we need to format the log at the filter level.
    This class provides a way to do that. It takes a formatter and applies it
    to the log. Here's an example use case:
        - When using the instrument-opentelemetry for logging,the formatter is
        never calledat the handler level.Therefore, we need to format the log at
        the filter level.
    """

    def __init__(
        self,
        formatter: logging.Formatter,
        name: str = "FormatFilter",
    ) -> None:
        super().__init__(name)
        self.formatter = formatter

    def filter(self, record: logging.LogRecord):
        record.msg = self.formatter.format(record)
        return True
