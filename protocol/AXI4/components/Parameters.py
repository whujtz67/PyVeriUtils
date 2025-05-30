from dataclasses import dataclass
from typing import Optional
import math

from pyVeriUtils.protocol.AXI4.spec.DutBundle import AxiBundleCfg


class AxiAgentCfg:
    def __init__(
        self,
        name: str,
        agentId: int,
        busBits: int = 512,
        MaxNrTxns: int = 8,
        randomTxn: bool = True,
        hasWr: bool = True,
        hasRd: bool = True,
        maxDataBytes: Optional[int] = None,
        bundleCfg: AxiBundleCfg = AxiBundleCfg(),
        timeout_threshold: int = 10000
    ):
        self.agentId = agentId
        self.busBits = busBits
        self.MaxNrTxns = MaxNrTxns
        self.randomTxn = randomTxn
        self.hasWr = hasWr
        self.hasRd = hasRd
        # In some cases, we don't want the data to be so large, which makes debug process more difficult.
        # As a result, we set the maxDataBytes.
        self.maxDataBytes = maxDataBytes

        self.busBytes = busBits >> 3
        self.busSize  = math.ceil(math.log2(self.busBytes))

        self.bundleCfg = bundleCfg
        self.timeout_threshold = timeout_threshold

class AxiTaskInfo:
   pass


