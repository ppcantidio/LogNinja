import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from examples.run_logs import run
from logninja import setup_logging
from logninja.configs import LogConsoleConfig, LogFileConfig
from logninja.ninja_formatter import NinjaFormatter
from logninja.ninja_rich_formatter import NinjaRichFormatter
from logninja.options import Only

setup_logging(
    log_file_config=LogFileConfig(
        filename="logs.log",
        clear_file_on_setup=True,
        level=logging.ERROR,
        fmt=NinjaFormatter(extras=None, max_message_length=None),
    ),
    log_console_config=LogConsoleConfig(
        level=logging.DEBUG,
        fmt=NinjaRichFormatter(extras=Only(keys=["X-Trace-Id"]), max_message_length=40),
    ),
)


logger = logging.getLogger("logninja")
run(logger=logger)
