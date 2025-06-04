from dataclasses import dataclass
from typing import Optional

# -------------------------------------
# Channel Configurations
# -------------------------------------
@dataclass
class AxCfg:
    has_lock: bool = False
    has_cache: bool = False
    has_prot: bool = False
    has_qos: bool = False
    has_region: bool = False
    has_user: bool = False

@dataclass
class WCfg:
    has_user: bool = False

@dataclass
class BCfg:
    has_user: bool = False

@dataclass
class RCfg:
    has_user: bool = False

class AxiBundleCfg:
    def __init__(self,
                 prefix="axi",
                 hierarchy=None,
                 aw=None,
                 w=None,
                 b=None,
                 ar=None,
                 r=None):
        self.prefix = prefix
        self.hierarchy = hierarchy

        # A None value for the Channel Cfg indicates that the bundle does not include this channel.
        self.aw = aw if aw is not None else AxCfg()
        self.w  = w  if w  is not None else WCfg()
        self.b  = b  if b  is not None else BCfg()
        self.ar = ar if ar is not None else AxCfg()
        self.r  = r  if r  is not None else RCfg()
