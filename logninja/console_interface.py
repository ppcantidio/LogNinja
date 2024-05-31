from abc import ABC, abstractmethod


class ConsoleInterface(ABC):
    """Abstract base class for console interfaces."""

    @abstractmethod
    def print(self, *objects: str, **kwargs):
        """Prints the given message to the console."""
        pass

    @abstractmethod
    def print_json(self, json: str, *args, **kwargs):
        """Prints the given message as JSON to the console."""
        pass

    @abstractmethod
    def print_exception(self, show_locals: bool = False):
        """Prints the exception to the console."""
        pass
