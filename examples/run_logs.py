import logging

from logninja.decorators import log_execution


@log_execution(level=logging.DEBUG, capture_exception=True, raise_exception=False)
def run(logger: logging.Logger) -> None:
    logger.info("Hello, world!", extra={"X-Trace-Id": "adfdfs", "x-user": "admin"})
    logger.debug(
        "Loading configuration file /adasd/asdasd/qeqwe/qwrqwrqwr/sdgsdgsdg/werwerwer/dfgerert/ertertert/ertetert/werwerwer"
    )
    logger.error("Unable to find 'pomelo' in database!")
    logger.info("POST /jsonrpc/ 200 65532")
    logger.info("POST /admin/ 401 42234")
    logger.warning("password was rejected for admin site.")
    logger.critical("Out of memory!")
    logger.info("Server exited with code=-1")

    number = 1
    divisor = 0
    foos = ["foo"] * 100
    logger.debug("in divide")
    number / divisor


def run_2(logger: logging.Logger) -> None:
    logger.info("Hello, world!", extra={"X-Trace-Id": "adfdfs", "x-user": "admin"})
    logger.debug(
        "Loading configuration file /adasd/asdasd/qeqwe/qwrqwrqwr/sdgsdgsdg/werwerwer/dfgerert/ertertert/ertetert/werwerwer"
    )
    logger.error(
        "Unable to find 'logninja' in database!", extra={"database": "defaultdb"}
    )
    logger.info("POST /jsonrpc/ 200 65532", extra={"client": "127.0.0.10"})
    logger.info("POST /admin/ 401 42234")
    logger.warning("password was rejected for admin site.")
    logger.critical("Out of memory!", extra={"memory": "100MB"})
    logger.info("Server exited with code=-1")
