from dataclasses import dataclass
from typing import Optional
from PyVeriUtils.SignalBinding.signalBinding import DecoupledIO
# from PyVeriUtils.protocol.AXI4.spec.Task import AxTask, WTask, RTask, BTask
from PyVeriUtils.protocol.AXI4.spec.DutBundleCfg import AxiBundleCfg, AxCfg, WCfg, RCfg, BCfg



# -------------------------------------
# DecoupledIO Bundles for Axi Channel
# -------------------------------------
class AxBundle(DecoupledIO):
    def __init__(
        self,
        dut,
        prefix: str,
        hierarchy: Optional[str] = None,
        cfg: AxCfg = AxCfg()
    ):
        base_fields = ["id", "addr", "len", "size", "burst"]
        optional_fields = [
            ("lock"  , cfg.has_lock  ),
            ("cache" , cfg.has_cache ),
            ("prot"  , cfg.has_prot  ),
            ("qos"   , cfg.has_qos   ),
            ("region", cfg.has_region),
            ("user"  , cfg.has_user  )
        ]
        fields = base_fields + [name for name, flag in optional_fields if flag]
        super().__init__(dut, fields, prefix, hierarchy)
        self.cfg = cfg

    def send(self, task):
        """
            Send tasks generated in env to dut.
        """
        self.bits.id.value    = task.flit.id
        self.bits.addr.value  = task.flit.addr
        self.bits.len.value   = task.flit.len
        self.bits.size.value  = task.flit.size
        self.bits.burst.value = task.flit.burst

        if self.cfg.has_lock:
            self.bits.lock.value = task.flit.lock
        if self.cfg.has_cache:
            self.bits.cache.value = task.flit.cache
        if self.cfg.has_prot:
            self.bits.prot.value = task.flit.prot
        if self.cfg.has_qos:
            self.bits.qos.value = task.flit.qos
        if self.cfg.has_region:
            self.bits.region.value = task.flit.region
        if self.cfg.has_user:
            self.bits.user.value = task.flit.user

        self.valid.value = 1
        


class WBundle(DecoupledIO):
    def __init__(
        self,
        dut,
        prefix: str,
        hierarchy: Optional[str] = None,
        cfg: WCfg = WCfg()
    ):
        base_fields = ["data", "strb", "last"]
        optional_fields = [
            ("user", cfg.has_user)
        ]
        fields = base_fields + [name for name, flag in optional_fields if flag]

        super().__init__(dut, fields, prefix, hierarchy)
        self.cfg = cfg

    def send(self, task):
        """
            Send tasks generated in env to dut.
        """
        bits = task.flit
        
        self.bits.data.value = task.flit.data()
        self.bits.strb.value = task.flit.strb()
        self.bits.last.value = task.flit.last()
        if self.cfg.has_user:
            self.bits.user.value = task.flit.user

        self.valid.value = 1


class RBundle(DecoupledIO):
    def __init__(
            self,
            dut,
            prefix: str,
            hierarchy: Optional[str] = None,
            cfg: RCfg = RCfg()
    ):
        base_fields = ["id", "data", "resp", "last"]
        optional_fields = [
            ("user", cfg.has_user)
        ]
        fields = base_fields + [name for name, flag in optional_fields if flag]

        super().__init__(dut, fields, prefix, hierarchy)
        self.cfg = cfg

    def send(self, task):
        """
            Send tasks generated in env to dut.
        """
        self.bits.id.value   = task.flit.id
        self.bits.data.value = task.flit.data()  # Beat index for burst transfers
        self.bits.resp.value = task.flit.resp
        self.bits.last.value = task.flit.last()

        if self.cfg.has_user:
            self.bits.user.value = task.flit.user

        self.valid.value = 1


class BBundle(DecoupledIO):
    def __init__(
            self,
            dut,
            prefix: str,
            hierarchy: Optional[str] = None,
            cfg: BCfg = BCfg()
    ):
        base_fields = ["id", "resp"]
        optional_fields = [
            ("user", cfg.has_user)
        ]
        fields = base_fields + [name for name, flag in optional_fields if flag]

        super().__init__(dut, fields, prefix, hierarchy)
        self.cfg = cfg

    def send(self, task):
        """
            Send tasks generated in env to dut.
        """
        self.bits.id.value = task.flit.id
        self.bits.resp.value = task.flit.resp

        if self.cfg.has_user:
            self.bits.user.value = task.flit.user

        self.valid.value = 1
        
class Axi4Bundle:
    def __init__(
            self,
            dut,
            cfg: AxiBundleCfg
    ) -> None:
        self.aw = AxBundle(dut, cfg.prefix, cfg.hierarchy, cfg.aw) if cfg.aw is not None else None
        self.w  = WBundle (dut, cfg.prefix, cfg.hierarchy, cfg.w ) if cfg.w  is not None else None
        self.b  = BBundle (dut, cfg.prefix, cfg.hierarchy, cfg.b ) if cfg.b  is not None else None
        self.ar = AxBundle(dut, cfg.prefix, cfg.hierarchy, cfg.ar) if cfg.ar is not None else None
        self.r  = RBundle (dut, cfg.prefix, cfg.hierarchy, cfg.r ) if cfg.r  is not None else None
