---
hide:
  - navigation
---
# *LogNinja*: Simple logging setup for Python
<p align="center">
   <a href="https://github.com/ppcantidio/LogNinja/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-C06524" alt="License: MIT" /></a>
   <a href="https://pypi.org/project/LogNinja/"><img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue" alt="Supported Python versions of the current PyPI release." /></a>
   <a href="https://www.pepy.tech/projects/LogNinja"><img src="https://static.pepy.tech/personalized-badge/LogNinja?&units=international_system&left_color=grey&right_color=blue&left_text=downloads" alt="Downloads" /></a>
</p>

<p align="center"><em>Simplified. Efficient. Customizable.</em></p>
LogNinja is a powerful library designed to simplify the configuration of logs in your Python applications. It provides an easy-to-use interface for setting up and managing logs, allowing you to focus on your application's functionality rather than the intricacies of logging.

One of the standout features of LogNinja is its ability to handle different configurations for console and file logs simultaneously. This means you can have one set of configurations for logs that are displayed on the console, and a different set for logs that are written to a file. This flexibility makes it easier to manage and control how your logs are generated and displayed, providing a more efficient debugging and monitoring process.

The library also supports JSON formatted logs, as shown in the basic usage example. This feature makes it easier to integrate your logs with other tools that can process JSON, providing more possibilities for log analysis and monitoring.

LogNinja also supports structured logging, which is a method of logging that provides more context and information than traditional flat logs. This can be particularly useful in complex systems where understanding the context of an event can be as important as the event itself. When used in conjunction with the Rich library, can produce colored logs. This can make your logs easier to read and understand, and can help you to identify errors and important information at a glance.

For applications using the ASGI standard, LogNinja offers a middleware for tracing logs per request. This feature allows you to track the lifecycle of each request, making it easier to identify issues and understand the performance of your application.

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

## License

This project is licensed under the terms of the MIT license.