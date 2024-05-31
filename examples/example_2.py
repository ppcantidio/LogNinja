import logging
import os
import sys

from logninja.ninja_console import NinjaConsole

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from examples.run_logs import run
from logninja import setup_logging
from logninja.configs import LogConsoleConfig, LogFileConfig
from logninja.ninja_json_formatter import NinjaJsonFormatter
from logninja.ninja_rich_console import NinjaRichConsole
from logninja.options import All

enviroment = "development"

if enviroment == "local":
    log_file_config = LogFileConfig(
        filename="logs.jsonl",
        clear_file_on_setup=True,
        level=logging.ERROR,
        fmt=NinjaJsonFormatter(extras=All()),
    )

    log_console_config = LogConsoleConfig(
        level=logging.DEBUG,
        fmt=NinjaJsonFormatter(extras=All()),
        console=NinjaRichConsole(),
        print_exeption=True,
        sys_excepthook=False,
    )
else:
    log_file_config = None

    log_console_config = LogConsoleConfig(
        level=logging.INFO,
        fmt=NinjaJsonFormatter(extras=All()),
        console=NinjaConsole(),
        print_exeption=True,
        sys_excepthook=False,
    )


setup_logging(log_file_config=log_file_config, log_console_config=log_console_config)


logger = logging.getLogger("logninja")
run(logger=logger)
