import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from examples.run_logs import run
from logninja import setup_logging
from logninja.configs import LogConsoleConfig, LogFileConfig
from logninja.ninja_json_formatter import NinjaJsonFormatter
from logninja.options import All

setup_logging(
    log_file_config=LogFileConfig(
        filename="logs.jsonl",
        clear_file_on_setup=True,
        level=logging.ERROR,
        fmt=NinjaJsonFormatter(extras=All()),
    ),
    log_console_config=LogConsoleConfig(
        level=logging.DEBUG,
        fmt=NinjaJsonFormatter(extras=All()),
    ),
)


logger = logging.getLogger("logninja")
run(logger=logger)
