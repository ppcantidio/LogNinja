import logging


class UvicornLoggerNameFilter(logging.Filter):
    """
    A logging filter that modifies the logger name for Uvicorn error records.

    This filter is used to change the logger name from "uvicorn.error" to "fastapi"
    for Uvicorn error records. It allows for more consistent and meaningful logging
    when using Uvicorn with FastAPI.

    Usage:
    ------
    Add an instance of this filter to the logger handlers that should apply the name change.

    Example:
    --------
    filter = UvicornLoggerNameFilter()
    logger.addFilter(filter)
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if record.name == "uvicorn.error":
            record.name = "fastapi"
        return True
