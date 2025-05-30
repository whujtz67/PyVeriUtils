class UpCounter:
    def __init__(self, start: int, end: int, name: str = "UpCounter"):
        assert (0 <= start) and (start < end)

        self.name = name
        self.count = start
        self.end = end

    def __str__(self):
        return f"{self.name}.count = {self.count}, {self.name}.end = {self.end}"

    def __iadd__(self, delta: int):
        self.count += delta

    def __isub__(self, delta: int):
        self.count -= delta

    def count_done(self):
        return self.count >= self.end
