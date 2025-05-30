from typing import Generic, TypeVar

T = TypeVar("T")

class Valid(Generic[T]):
    def __init__(self, bits: T):
        self.bits: T = bits
        self.valid: bool = False