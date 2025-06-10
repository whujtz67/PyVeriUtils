class IdPool:
    ID_EMPTY = 677

    def __init__(self, size, name="id pool", start = 0):
        self.pool  = list(range(start, size + start))
        self.start = start
        self.size  = size
        self.name  = name

    def list(self):
        """
            List all the available id
        """
        print(f"{self.name} available id:\n\t|", end='')
        for id in self.pool:
            print(f"{id:^5}", end='|')  # :^3 central align 3 characters
        print()
        return self.pool

    def allocate(self, id=None):
        # allocate a specific given id
        if id is not None:
            if id in self.pool:
                self.pool.remove(id)
                return id
            else:
                assert False, f"trying to alloc a non-exist id ==> {id}"
        else:
            if self.is_empty():
                return self.ID_EMPTY
            # id == None, which means the task hasn't been allocated an id
            else:
                return self.pool.pop()  # if id = None, randomly allocate an id from id pool

    def release(self, id: int):
        if id in self.pool:
            raise ValueError(f'id {id} is already in {self.name}')
        self.pool.append(id)

    def release_all(self):
        self.pool = list(range(self.start, self.size + self.start))

    def is_empty(self):
        return len(self.pool) == 0