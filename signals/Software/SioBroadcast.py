from typing import List, Generic, TypeVar
from enum import Enum

from PyVeriUtils.signals.Software.SoftwareIO import sValidIO, sDecoupledIO

T = TypeVar('T')

class SioBroadcast(Generic[T]):
    """
    This class implements a standalone broadcast module instead of using return-based signal passing between modules.
    It improves code readability, reusability, and robustness, and avoids issues such as duplicated requests.
    """
    class State(Enum):
        IDLE = 0
        BROADCASTING = 1

    def __init__(
            self,
            mst: sValidIO[T],
            slvs: List[sDecoupledIO[T]]
    ):
        self.mst: sValidIO[T] = mst
        self.slvs: List[sDecoupledIO[T]] = slvs

        self.slvs_fired: List[bool] = [False] * len(slvs)
        self.state = self.State.IDLE

    def broadcast(self):
        """
        A simple FSM is used to improve code clarity.

        We do not adopt the full three-stage FSM structure common in hardware for the following reasons:
        1. The FSM here is very simple, and the current structure does not significantly harm readability.
        2. In software, state changes take effect immediately, making it hard to decouple state transitions from output logic
           unless we explicitly introduce separate registers for current and next states (e.g., state_r and state_nxt).
           However, doing so would complicate the code unnecessarily. For more complex FSMs, that pattern may be worth considering.
        """
        if self.state == self.State.IDLE:
            if self.mst.valid:
                self.state = self.State.BROADCASTING

        elif self.state == self.State.BROADCASTING:
            if all(self.slvs_fired):
                # In strict hardware-style valid-ready handshaking, masters and slaves should not control each other's signals.
                # However, in software we can simplify things by directly deasserting master.valid here.
                # This removes the need for the master to observe ready or implement response tracking logic.
                self.mst.valid = False
                self.slvs_fired = [False] * len(self.slvs)
                self.state = self.State.IDLE
                return

            for i in range(len(self.slvs)):
                if not self.slvs_fired[i]:
                    self.slvs[i].bits = self.mst.bits
                    self.slvs[i].valid = True

                    if self.slvs[i].fire():
                        self.slvs_fired[i] = True
                else:
                    self.slvs[i].bits = None
                    self.slvs[i].valid = False
        else:
            assert False, f"Unexpected state {self.state}"


# TODO: 1-to-1 broadcast
