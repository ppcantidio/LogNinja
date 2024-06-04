---
hide:
  - navigation
---
# Formatters
Formatters are responsible for converting log records into text strings that can be displayed to the user or written to a file. A formatter typically takes a log record (an object that contains information about a logging event, such as the message, severity, timestamp, etc.) and returns a formatted string. They are tipcally called by our Handlers, at the case of LogNinja, more escifically by `NinjaHandler`. LogNinja provide some formatter that can be usefull, they are following the interface `logging.Formatter`.

## NinjaFormatter
The `NinjaFormatter` is a custom formatter provided by the LogNinja library. It is designed to format log messages in a simple and readable way, making it ideal for use in cloud environments where simplicity and readability are key.
Here is an example of how to use the `NinjaFormatter`:
```python
from logninja import setup_logging
from logninja.configs import LogConsoleConfig
from logninja.ninja_formatter import NinjaFormatter
from logninja.consoles import NinjaRichConsole
from logninja.options import All

log_console_config = LogConsoleConfig(
    level=logging.INFO,
    fmt=NinjaFormatter(
        extras=All(),
        max_message_length=40,
    ),
    console=NinjaRichConsole()
)

setup_logging(log_console_config=log_console_config)
```

Output:


## NinjaJsonFormatter
The `NinjaJsonFormatter` is another custom formatter provided by the LogNinja library. As the name suggests, it formats log messages as JSON objects. This can be particularly useful when you need to process your logs programmatically, as JSON is a widely supported format that can be easily parsed and manipulated.

Here is an example of how to use the NinjaJsonFormatter:
```python
from logninja import setup_logging
from logninja.configs import LogConsoleConfig
from logninja.ninja_json_formatter import NinjaJsonFormatter
from logninja.options import All

log_console_config = LogConsoleConfig(
    level=logging.INFO,
    fmt=NinjaJsonFormatter(extras=All()),
)

setup_logging(log_console_config=log_console_config)
```

With levels `INFO`, `DEBUG`:

When some exceptions occurer:

