from typing import List


class All:
    def __repr__(self):
        return "All()"


class Only:
    def __init__(self, keys: List[str]):
        if not isinstance(keys, list):
            raise ValueError("keys must be a list")
        self.extras = keys

    def __repr__(self):
        return f"Only({self.extras})"
