from collections import deque


class IdPool:
    """
    A pool for managing unique integer IDs with efficient allocation and release operations.

    Uses a deque for O(1) operations on both ends. Note that after multiple allocations
    and releases, the order of IDs in the pool may not be sorted numerically due to the
    release mechanism appending IDs to the right end.

    Attributes:
        ID_EMPTY (int): Special value returned when pool is empty
        pool (deque): Available IDs in the pool
        start (int): Starting value for ID range
        size (int): Total number of IDs in the pool
        name (str): Descriptive name for the pool
    """

    ID_EMPTY = 677

    def __init__(self, size, name="id pool", start=0):
        """
        Initialize the ID pool with a range of IDs.

        Args:
            size: Number of IDs in the pool
            name: Descriptive name for the pool (default "id pool")
            start: Starting value for ID range (default 0)
        """
        self.pool = deque(range(start, size + start))
        self.start = start
        self.size = size
        self.name = name

    def list(self):
        """
        Print and return all available IDs in the pool.
        """
        print(f"{self.name} available id:\n\t|", end='')
        for id in self.pool:
            print(f"{id:^5}", end='|')  # :^5 central align 5 characters
        return list(self.pool)  # Convert to list for external use

    def allocate(self, id=None):
        """
        Allocate an ID from the pool.

        Args:
            id: Specific ID to allocate (optional). If not provided,
                allocates the leftmost ID (O(1) operation).

        Returns:
            int: Allocated ID or ID_EMPTY if pool is empty
        """
        if id is not None:
            # Handle specific ID request
            if id in self.pool:
                self.pool.remove(id)  # O(n) operation
                return id
            else:
                assert False, f"trying to alloc a non-exist id ==> {id}"
        else:
            # Handle generic allocation request
            if self.is_empty():
                return self.ID_EMPTY
            return self.pool.popleft()  # O(1) operation

    def release(self, id: int):
        """
        Release an ID back to the pool.

        Note: Released IDs are appended to the right end, which may
        result in non-sorted order after multiple operations.
        """
        if id in self.pool:
            raise ValueError(f'id {id} is already in {self.name}')
        self.pool.append(id)  # O(1) operation

    def reset_pool(self):
        """Reset the pool to its initial state with all IDs."""
        self.pool = deque(range(self.start, self.size + self.start))

    def is_empty(self):
        """Check if the pool is empty."""
        return len(self.pool) == 0