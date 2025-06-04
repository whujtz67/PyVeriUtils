from PyVeriUtils.protocol.AXI4.components.Parameters import AxiAgentCfg
from PyVeriUtils.protocol.AXI4.spec.DutBundle import Axi4Bundle
from PyVeriUtils.protocol.AXI4.spec.Task import AxTask, WTask, RTask, BTask
from PyVeriUtils.utils.Common.Queue import Queue


class BaseAxiMaster:
    """
    A base class for AXI4 master agents in cocotb-based simulations.

    This class provides a minimal working skeleton of an AXI master,
    including basic infrastructure such as task queues and channel interfaces.

    Subclasses are expected to implement custom behavior as needed,
    particularly in the `drive_phase()` and `sample_phase()` methods,
    which together form the core of the transaction-level simulation loop.

    - `drive_phase()` should be called in the first delta cycle after a clock edge to drive signals.
    - `sample_phase()` should be called in the second delta cycle to capture DUT responses.

    This class is not meant to represent a fully featured AXI master,
    but rather to serve as a reusable and extensible base for more specialized agents.
    """
    def __init__(
            self,
            dut,
            name: str,
            cfg: AxiAgentCfg
    ) -> None:
        self.dut = dut
        self.name = name
        self.cfg: AxiAgentCfg = cfg
        self.io = Axi4Bundle(dut, cfg.bundleCfg)

        self.aw_queue: Queue[AxTask] = Queue[AxTask](2) # The depth doesn't need to be so large, ping-pong buffer is enough.
        self.w_queue : Queue[WTask ] = Queue[WTask ](2)
        self.ar_queue: Queue[AxTask] = Queue[AxTask](2)

        self.r_queue: Queue[RTask] = Queue[RTask](1)
        self.b_queue: Queue[BTask] = Queue[BTask](1)

    def req_alloc(self):
        pass

    def set_rx_ready(self):
        """
        By default, as long as the B/R channel Queue has available slots
        it can always accept responses from the B/R channels,
        meaning the ready signals for the B/R channels are asserted high persistently.

        However, subclasses can implement customized handling,
        such as introducing delays or other logic modifications.
        """
        self.io.b.ready.value = int(not self.b_queue.is_full())
        self.io.r.ready.value = int(not self.r_queue.is_full())

    def send(self):
        if not self.aw_queue.is_empty():
            self.io.aw.send(self.aw_queue.peek())
        else:
            self.io.aw.valid.value = 0

        if not self.w_queue.is_empty():
            self.io.w.send(self.w_queue.peek())
        else:
            self.io.w.valid.value = 0

        if not self.aw_queue.is_empty():
            self.io.ar.send(self.ar_queue.peek())
        else:
            self.io.ar.valid.value = 0

    def recv(self):
        if self.io.r.fire():
            self.r_queue.enq(
                RTask.recv(
                    bdl = self.io.r,
                    alloc_cycle = self.dut.cycles.value.integer,
                    timeout_threshold = self.cfg.timeout_threshold,
                    label = self.name
            ))

        if self.io.b.fire():
            self.b_queue.enq(
                BTask.recv(
                    bdl = self.io.b,
                    alloc_cycle = self.dut.cycles.value.integer,
                    timeout_threshold = self.cfg.timeout_threshold,
                    label = self.name
            ))

    def drive_phase(self):
        """
        Delta-cycle phase 1: drive inputs to the DUT.

        This method is intended to be called *immediately after* a clock edge,
        during the first delta cycle of a simulation step.

        It performs:
          - Task allocation (if any)
          - Driving valid signals for AW/W/AR channels
          - Asserting ready signals for B/R channels based on queue availability
        """
        self.req_alloc()

        self.send()
        self.set_rx_ready()

    def sample_phase(self):
        """
        Delta-cycle phase 2: sample outputs from the DUT.

        This method should be called during the *second delta cycle*
        of a simulation step, after input changes have propagated.

        It checks whether the B or R channels have valid responses
        and enqueues them as tasks.

        This must follow the `drive_phase()` in the same simulation cycle.
        """
        self.recv()



