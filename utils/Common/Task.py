from pyVeriUtils.utils.Logger.Logger import BaseLogger

class BaseTask(BaseLogger):
    def __init__(
            self,
            name: str,
            alloc_cycle: int,
            timeout_threshold: int
    ):
        self.name = name
        self.alloc_cycle = alloc_cycle
        self.timeout_cnt = 0
        self.timeout_threshold = timeout_threshold

    def __str__(self):
        return f"[Task {self.name}] {self.list_attr_exc('name')}"

    def timeout_check(self):
        self.timeout_cnt += 1

        if self.timeout_cnt == self.timeout_threshold:
            raise TimeoutError(f"[Timeout!!!] {self}")
