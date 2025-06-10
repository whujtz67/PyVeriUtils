from typing import Generic, Deque, TypeVar, Optional
from collections import deque

T = TypeVar('T')

class Queue(Generic[T]):
    def __init__(
            self,
            depth: Optional[int] = None,
            label: Optional[str] = None
    ):
        if depth is not None:
            assert depth > 0, "The depth of the queue should be greater than zero!"

        self.name: str = f"{label}_Queue" if label is not None else "Queue"

        self.queue: Deque[T] = deque()
        self.depth: Optional[int] = depth

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def is_full(self) -> bool:
        return len(self.queue) == self.depth if self.depth is not None else False

    def enq(self, bits: T) -> None:
        assert not self.is_full(), "The queue is already full!"

        self.queue.append(bits)

    def deq(self) -> None:
        self.queue.popleft()

    def peek(self) -> T:
        return self.queue[0]

    def rear(self) -> T:
        return self.queue[-1]

    def len(self) -> int:
        return len(self.queue)