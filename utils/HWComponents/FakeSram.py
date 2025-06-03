from typing import List
class FakeSram:
    def __init__(self, depth: int, name: str = "SRAM") -> None:
        self.name  = name
        self.depth = depth
        self.rams  = [0] * depth

    def read(self, addr: int) -> int:
        return self.rams[addr]

    def write(self, addr: int, data: int) -> None:
        self.rams[addr] = data

    def dump(self, addr: int) -> str:
        return f"{self.name}[{addr}] = {hex(self.read(addr))}"

    def dump_all(self) -> str:
        return "\n".join([self.dump(addr) for addr in range(self.depth)])

class FakeSramArray:
    def __init__(self, depth: int, bank: int, name: str = "SRAMs") -> None:
        self.depth = depth
        self.bank = bank
        self.name = name
        self.srams = [
            FakeSram(depth=depth, name=f"{name}_bank_{i}") for i in range(bank)
        ]

    def read(self, bank_id: int, addr: int) -> int:
        return self.srams[bank_id].read(addr)

    def read_set(self, addr: int) -> List[int]:
        return [sram.read(addr) for sram in self.srams]

    def write(self, bank_id: int, addr: int, data: int) -> None:
        self.srams[bank_id].write(addr, data)

    def write_set(self, addr: int, datas: List[int]) -> None:
        assert len(datas) == self.bank, \
            f"Expected {self.bank} elements in datas, got {len(datas)}"
        for i, data in enumerate(datas):
            self.srams[i].write(addr, data)

    def dump(self, bank_id: int, addr: int) -> str:
        return self.srams[bank_id].dump(addr)

    def dump_bank(self, bank_id: int) -> str:
        return self.srams[bank_id].dump_all()

    def dump_set(self, addr: int) -> str:
        return "\n".join([sram.dump(addr) for sram in self.srams])

    def dump_all(self) -> str:
        return "\n\n".join([self.dump_bank(i) for i in range(self.bank)])


