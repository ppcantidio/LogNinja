# *LogNinja*: Simple logging setup for Python
<p align="center">
   <a href="https://github.com/ppcantidio/LogNinja/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-C06524" alt="License: MIT" /></a>
   <a href="https://pypi.org/project/LogNinja/"><img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue" alt="Supported Python versions of the current PyPI release." /></a>
   <a href="https://www.pepy.tech/projects/LogNinja"><img src="https://static.pepy.tech/personalized-badge/LogNinja?&units=international_system&left_color=grey&right_color=blue&left_text=downloads" alt="Downloads" /></a>
</p>

<p align="center"><em>Simplified. Efficient. Customizable.</em></p>
LogNinja is a simple logging setup to be used in Python applications.

## Installation

To install LogNinja, use pip:
```sh
pip install logninja
```

## Basic Usage
First, set up LogNinja:
```python
from logninja import setup_logging
from logninja.configs import LogConsoleConfig

setup_logging(log_console_config=LogConsoleConfig())
```

This basic setup will format all your logs as JSON.

## Advanced Usage
### Setup
LogNinja's setup also provides advanced logging features, such as ContextVars, custom formatters, and custom log levels.
#### Example:
```python
import logging

from my_custom_formatter import CustomFormatter
from my_globals_contextvar import trace_id

from logninja import setup_logging
from logninja.configs import LogConsoleConfig

setup_logging(
    contextvars=[trace_id],
    log_file_config=LogConsoleConfig(),
)
```

The context variables will be automatically set for all logs. This allows you to use trace logs with your custom context variables.

### ASGI Middleware
If you're developing an ASGI application, you can use the LogNinjaASGIMiddleware to automatically log requests and responses:
```python
from my_globals_contextvar import trace_id
from my_logger import logger

from logninja.asgi.middleware import LogNinjaASGIMiddleware

app = FastAPI()
app.add_middleware(
    LogNinjaASGIMiddleware,
    logger=logger,
    contextvars_by_headers=[(request_id, "X-Request-ID")],
)
```

This allows you to capture the contextvars from headers and, combined with the `setup_logging(contextvars=[trace_id])`, creates a powerful tool to capture trace IDs from the headers and use them in all logs within the ASGI request context.

### Decorator
The `log_execution` decorator is a powerful tool provided by LogNinja to log the execution time of a function or coroutine.

Here is an example of how to use it:

```python
from logninja import log_execution

@log_execution()
def my_function():
    # Your code here
    pass
```

This will automatically log the start and end of the function execution, as well as the total execution time.

The decorator can also be used with coroutines:
```python
from logninja import log_execution


@log_execution()
async def my_coroutine():
    # Your code here
    pass
```
In both cases, the decorator uses the LogNinja logger by default, but you can provide your own logger if you prefer:
```python
from my_logger import logger

from logninja import log_execution


@log_execution(logger=logger)
async def my_coroutine():
    # Your code here
    pass
```

When you use the `log_execution` decorator, it generates logs at the start and end of the function or coroutine execution. Here are examples of what these logs look like in both console and JSON formats.

#### Ninja Format
With ninja format, the logs are displayed as plain text. Here's an example:

```plaintext
['2024-05-30 18:58:28'] [DEBUG   ] 'my_function' executed in 0.0183 seconds   [logninja] decorators.py:55
['2024-05-30 18:58:28'] [DEBUG   ] 'my_function' executed in 0.0183 seconds   [logninja] decorators.py:55
```

### Ninja JSON Format
In the JSON format, the logs are displayed as JSON objects. Here's an example:
```json
{
  "level": "INFO",
  "logger": "logninja",
  "message": "Starting execution of function my_function",
  "params": {
    "args": [],
    "kwargs": {}
  }
}

{
  "level": "INFO",
  "logger": "logninja",
  "message": "my_function executed in 0.0020 seconds"
}
```
The JSON logs contain the same information as the console logs, but they also include the log level, the logger name, and any extra parameters that were passed to the function or coroutine.

### Format Exceptions
All logged exceptions are automatically formatted by our `NinjaJsonFormatter`:
```python
import logging

from logninja import setup_logging

setup_logging()

logger = logging.getLogger("my_logger")

try:
    1 / 0
except Exception as exc_info:
    logger.exception("Unexpected error", exc_info=exc_info)
```
By passing the `exc_info`, LogNinja automatically builds a JSON log like this:

```json
{
  "level": "ERROR",
  "message": "Unexpected error",
  "timestamp": "2024-05-24T19:51:31.402206+00:00",
  "logger": "my_logger",
  "module": "teste",
  "function": "<module>",
  "line": 12,
  "thread_name": "MainThread",
  "exc_info": [
    {
      "exc_type": "ZeroDivisionError",
      "exc_value": "division by zero",
      "syntax_error": null,
      "is_cause": false,
      "frames": [
        {
          "filename": "path_here",
          "logger": "my_logger",
          "module": "teste",
          "function": "<module>",
          "line": 12,
          "thread_name": "MainThread",
          "exc_info": [
            {
              "exc_type": "ZeroDivisionError",
              "exc_value": "division by zero",
              "syntax_error": null,
              "is_cause": false,
              "frames": [
                {
                  "filename": "path_here",
                  "lineno": 10,
                  "name": "<module>",
                  "line": "",
                  "locals": {
                    "__name__": "__main__",
                    "__doc__": "None",
                    "__package__": "None",
                    "__loader__": "<_frozen_importlib_external.SourceFileLoader object at 0x000001FDA90251D0>",
                    "__spec__": "None",
                    "__annotations__": "{}",
                    "__builtins__": "<module 'builtins' (built-in)>",
                    "__file__": "path_here",
                    "__cached__": "None",
                    "logging": "path_here",
                    "setup_logging": "<function setup_logging at 0x000001FDA91BA7A0>",
                    "logger": "<Logger my_logger (INFO)>",
                    "exc_info": "ZeroDivisionError('division by zero')"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```
**Important Notice**: This functionality contains code derived from the `structlog` project, available at https://github.com/hynek/structlog. Changes were made starting from May 24th, 2024. The original code is licensed under the MIT License or Apache-2.0. Please ensure to comply with these licenses when using LogNinja.

## License
This project is licensed under the terms of the MIT license.