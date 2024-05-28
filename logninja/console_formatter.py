from logging import Formatter

ConsoleFormatter = Formatter(
    fmt="[%(name)s][%(levelname)s]: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
)
