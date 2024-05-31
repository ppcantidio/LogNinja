from abc import ABC, abstractmethod


class ConsoleInterface(ABC):
    @abstractmethod
    def print(self, message: str):
        pass

    @abstractmethod
    def print_json(self, message: str):
        pass
