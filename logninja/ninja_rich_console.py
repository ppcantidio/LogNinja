import re
from typing import List

try:
    from rich.console import Console
except ImportError:
    raise ImportError(
        "rich library is required for NinjaRichConsole, install it with pip install rich"
    )

HTTP_METHODS: List[str] = [
    "GET",
    "POST",
    "HEAD",
    "PUT",
    "DELETE",
    "OPTIONS",
    "TRACE",
    "PATCH",
]


class NinjaRichConsole(Console):
    def print(self, *objects: str, **kwargs) -> None:
        if all(isinstance(i, str) for i in objects):
            objects = [self._custom_theme(i) for i in objects]
            message = "".join(objects)
            super().print(message, **kwargs)
            return
        super().print(*objects, **kwargs)

    def _custom_theme(self, message: str) -> str:
        message = self._replace_loglevel(message)
        message = self._replace_datetime(message)
        message = self._replace_file_line(message)
        message = self._replace_parentheses_content(message)
        message = self._replace_extras(message)
        message = self._highlight_msg(message)
        return message

    def _replace_loglevel(self, message: str) -> str:
        message = message.replace("[DEBUG   ]", "[blue][DEBUG   ][/blue]")
        message = message.replace("[INFO    ]", "[green][INFO    ][/green]")
        message = message.replace("[WARNING ]", "[yellow][WARNING ][/yellow]")
        message = message.replace("[ERROR   ]", "[bold red][ERROR   ][/bold red]")
        message = message.replace("[CRITICAL]", "[bold red][CRITICAL][/bold red]")
        return message

    def _replace_datetime(self, message: str) -> str:
        string = re.sub(
            r"(\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\])", r"[dim]\g<0>[/dim]", message
        )
        return string

    def _replace_file_line(self, message: str):
        string = re.sub(
            r"(\w+\.py:\d+)", r"[dim underline]\g<0>[/dim underline]", message
        )
        return string

    def _replace_parentheses_content(self, message: str) -> str:
        message = re.sub(r"(\(\w+\))", r"[orange4]\g<0>[/orange4]", message)
        return message

    def _replace_extras(self, message: str) -> str:
        result = re.sub(r"(?<=\=)([\w-]+)", r"[blue]\g<0>[/blue]", message)
        result = re.sub(r"([\w-]+)(?=\=)", r"[yellow]\g<0>[/yellow]", result)
        return result

    def _highlight_msg(self, message: str) -> str:
        message = self._highlight_http_status_codes(message)
        message = self._highlight_http_methods(message)
        return message

    def _highlight_http_methods(self, message: str) -> str:
        for method in HTTP_METHODS:
            if method in message:
                message = message.replace(method, f"[bold]{method}[/bold]")
        return message

    def _highlight_http_status_codes(self, message: str) -> str:
        status_codes = {
            "1..": "blue",  # Informational
            "2..": "green",  # Success
            "3..": "yellow",  # Redirection
            "4..": "red",  # Client errors
            "5..": "magenta",  # Server errors
        }

        for status_code, color in status_codes.items():
            status_code_pattern = status_code.replace("..", "\d\d")
            pattern = re.compile(rf"\b{status_code_pattern}\b")
            matches = pattern.findall(message)
            for match in matches:
                message = message.replace(
                    match, f"[bold {color}]{match}[/bold {color}]"
                )
        return message
