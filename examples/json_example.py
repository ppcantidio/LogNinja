import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from examples.run_logs import run
from logninja import setup_logging
from logninja.configs import LogConsoleConfig, LogConsoleType, LogFileConfig
from logninja.json_formatter import JSONFormatter

setup_logging(
    log_file_config=LogFileConfig(
        filename="logs.jsonl",
        clear_file_on_setup=True,
        level=logging.ERROR,
        fmt=JSONFormatter(),
    ),
    log_console_config=LogConsoleConfig(
        level=logging.DEBUG,
        log_console_type=LogConsoleType.JSON,
        extra_vars=["x-Trace-Id"],
    ),
)


logger = logging.getLogger("logninja")
run(logger=logger)
