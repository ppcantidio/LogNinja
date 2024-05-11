from logging import Formatter

ConsoleFormatter = Formatter(
    format="%(levelname)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
)
