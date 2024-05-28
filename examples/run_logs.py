import logging


def run(logger: logging.Logger) -> None:
    logger.info("Hello, world!", extra={"x-Trace-Id": "adfdfs"})
    logger.debug(
        "Loading configuration file /adasd/asdasd/qeqwe/qwrqwrqwr/sdgsdgsdg/werwerwer/dfgerert/ertertert/ertetert/werwerwer"
    )
    logger.error("Unable to find 'pomelo' in database!")
    logger.info("POST /jsonrpc/ 200 65532")
    logger.info("POST /admin/ 401 42234")
    logger.warning("password was rejected for admin site.")
    logger.critical("Out of memory!")
    logger.info("Server exited with code=-1")

    def divide() -> None:
        number = 1
        divisor = 0
        foos = ["foo"] * 100
        logger.debug("in divide")
        try:
            number / divisor
        except:
            logger.exception("An error of some kind occurred!")

    divide()
