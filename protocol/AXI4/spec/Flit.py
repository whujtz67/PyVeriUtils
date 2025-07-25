# Define some commonly used Classes
from dataclasses import dataclass
import random
from typing import List, Generic, TypeVar, Optional, Tuple
from PyVeriUtils.protocol.AXI4.spec.Encodings import BurstType, RespType

from PyVeriUtils.protocol.AXI4.spec.DutBundle import AxBundle, WBundle, RBundle, BBundle

T = TypeVar('T')

# ========================================
# Define AXI4 Flit for each channel
# ========================================
@dataclass
class AxFlit(Generic[T]):
    id    : int
    addr  : int
    len   : int
    size  : int
    burst : BurstType = BurstType.INCR
    lock  : Optional[int] = None
    cache : Optional[int] = None
    prot  : Optional[int] = None
    qos   : Optional[int] = None
    region: Optional[int] = None
    user  : Optional[T]   = None

    @classmethod
    def random_gen(
        cls,
        id_bits: int,
        addr_range: Tuple[int, int],
        max_len: int,
        max_size: int,
        bus_size: int
    ) -> "AxFlit":
        min_addr, max_addr = addr_range

        id   = random.randint(0, (1 << id_bits) - 1) # same ID is allowed
        addr = random.randint(min_addr, max_addr) >> bus_size << bus_size
        len  = random.randint(0, max_len)
        size = random.randint(0, max_size)

        # we don't consider user in random_gen
        return cls(id, addr, len, size)

    @classmethod
    def recv(cls, bdl: AxBundle) -> "AxFlit":
        return cls(
            id     = bdl.bits.id.value,
            addr   = bdl.bits.addr.value,
            len    = bdl.bits.len.value,
            size   = bdl.bits.size.value,
            burst  = BurstType.int_to_enum(int(bdl.bits.burst.value)),
            lock   = bdl.bits.lock.value if bdl.cfg.has_lock else None,
            cache  = bdl.bits.cache.value if bdl.cfg.has_cache else None,
            prot   = bdl.bits.prot.value if bdl.cfg.has_prot else None,
            qos    = bdl.bits.qos.value if bdl.cfg.has_qos else None,
            region = bdl.bits.region.value if bdl.cfg.has_region else None,
            user   = bdl.bits.user.value if bdl.cfg.has_user else None,
        )


@dataclass
class WFlit(Generic[T]):
    data: int
    strb: int
    last: bool
    user: Optional[T] = None

    @classmethod
    def recv(cls, bdl: WBundle) -> "WFlit":
        return cls(
            data = bdl.bits.data.value,
            strb = bdl.bits.strb.value,
            last = bool(bdl.bits.last.value),
            user = bdl.bits.user.value if bdl.cfg.has_user else None,
        )

@dataclass
class RFlit(Generic[T]):
    id: int
    data: int
    resp: RespType
    last: bool
    user: Optional[T] = None

    @classmethod
    def recv(cls, bdl: RBundle) -> "RFlit":
        return cls(
            id   = bdl.bits.id.value,
            data = bdl.bits.data.value,
            resp = bdl.bits.resp.value,
            last = bool(bdl.bits.last.value),
            user = bdl.bits.user.value if bdl.cfg.has_user else None,
        )

@dataclass
class BFlit(Generic[T]):
    id: int
    resp: RespType = RespType.OKAY
    user: Optional[T] = None

    @classmethod
    def random_gen(cls, aw: AxFlit) -> "BFlit":
        # Not randomized actually, just to keep consistent with other channels.
        return cls(aw.id)

    @classmethod
    def recv(cls, bdl: BBundle) -> "BFlit":
        return cls(
            id   = bdl.bits.id.value,
            resp = bdl.bits.resp.value,
            user = bdl.bits.user.value if bdl.cfg.has_user else None,
        )


@dataclass
class WBatch(Generic[T]):
    datas: List[int]
    strbs: List[int]
    beat: int = 0
    user: Optional[T] = None

    def last(self) -> bool:
        return self.beat == (len(self.datas) - 1)

    def data(self) -> int:
        return self.datas[self.beat]

    def strb(self) -> int:
        return self.strbs[self.beat]
    
    def beat_incr(self) -> None:
        self.beat += 1

    @classmethod
    def random_gen(
            cls,
            nr_beats: int,
            size: int,
            bus_size: int,
            max_size: Optional[int] = None
    ) -> "WBatch":
        actual_data_size = min(size, max_size) if max_size is not None else size
        nr_data_bits = 1 << (actual_data_size + 3)
        max_data = (1 << nr_data_bits) - 1
        bus_bytes = 1 << bus_size

        # TODO: Not finished

@dataclass
class RBatch(Generic[T]):
    id: int
    datas: List[int]
    resp: RespType = RespType.OKAY
    beat: int = 0
    user: Optional[T] = None

    def last(self) -> bool:
        return self.beat == (len(self.datas) - 1)

    def data(self) -> int:
        # print(f"datas = {self.datas}")
        # print(f"Send R data {self.datas[self.beat]}")
        return self.datas[self.beat]
    
    def beat_incr(self) -> None:
        self.beat += 1

    @classmethod
    def random_gen(
            cls,
            ar: AxFlit,
            maxDataBytes: int,
            busSize: int
    ) -> "RBatch":
        beat_bytes = 1 << ar.size
        data_bytes = min(beat_bytes, maxDataBytes) if maxDataBytes is not None else beat_bytes
        data_bits  = data_bytes << 3
        max_data   = (1 << data_bits) - 1

        bus_bytes = 1 << busSize
        bus_bits  = bus_bytes << 3

        bus_off_mask = (1 << busSize) - 1
        base_offset = ar.addr & bus_off_mask

        bus_data_mask = (1 << bus_bits) - 1  # The data generated should not be greater than bus_data_mask!

        datas = []

        beat_offset = base_offset

        # print(f"[RANDOM_GEN_RBatch] AR addr = {hex(ar.addr)}, id = {hex(ar.id)}, size = {hex(ar.size)}, len = {ar.len}")

        for i in range(ar.len + 1):
            valid_data   = random.randint(0, max_data)
            data_off     = beat_offset << 3
            shifted_data = valid_data << data_off
            data         = shifted_data & bus_data_mask
            datas.append(data)

            # print(f"[RANDOM_GEN_RBatch] Beat {i}: beat_offset = {beat_offset}, data = {hex(data)}")

            beat_offset = 0 if (beat_offset + beat_bytes) >= bus_bytes else beat_offset + beat_bytes

        return cls(ar.id, datas)