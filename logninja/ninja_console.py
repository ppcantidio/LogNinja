class NinjaConsole:
    terminator = "\n"

    def __init__(self, stream) -> None:
        self.stream = stream

    def print(self, message: str):
        try:
            stream = self.stream
            stream.write(message + self.terminator)
        except RecursionError:
            raise
