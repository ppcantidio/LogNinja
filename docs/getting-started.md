---
hide:
  - navigation
---
# Getting Started with LogNinja
## Installation
To install LogNinja, you can use pip, the Python package installer. Run the following command in your terminal:
```sh
pip install logninja
```
Ensure that you have pip installed and that it is updated to its latest version. If not, you can install pip by following the instructions on the official pip installation guide.

## Your First Log Entry
```python
import logging

from logninja import setup_logging
from logninja.configs import LogConsoleConfig
from logninja.consoles import NinjaConsole
from logninja.ninja_formatter import NinjaFormatter
from logninja.options import All

# Set up logging
setup_logging(
    log_console_config=LogConsoleConfig(
        level=logging.DEBUG,
        fmt=NinjaFormatter(extras=All(), max_message_length=40),
        console=NinjaConsole(),
    ),
)

# Create a logger
logger = logging.getLogger(__name__)

# Log an info message
logger.info("This is my first log entry!")

```
### Output Example
![Output Example](assets/table.svg)