from PyVeriUtils.protocol.AXI4.components.Parameters import AxiAgentCfg
from PyVeriUtils.protocol.AXI4.spec.DutBundle import Axi4Bundle
from PyVeriUtils.protocol.AXI4.spec.Task import AxTask, WTask, RTask, BTask
from PyVeriUtils.utils.Common.Queue import Queue
from PyVeriUtils.protocol.AXI4.spec.Encodings import Channel

class BaseAxiSlave:
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

        # B/R response queues with no depth limit for simplicity.
        # Since AW/AR queues have bounded depth, the number of B/R tasks
        # will naturally remain small in practice.
        self.r_queue: Queue[RTask] = Queue[RTask](depth = None)
        self.b_queue: Queue[BTask] = Queue[BTask](depth = None)

        # AW/AR request queues used for response allocation.
        # Dequeued when the corresponding B/R response is allocated.
        self.aw_queue: Queue[AxTask] = Queue[AxTask](2)
        self.ar_queue: Queue[AxTask] = Queue[AxTask](2)

        # AW/AR check queues used for protocol checking.
        # Dequeued immediately after the request is checked.
        #
        # Separate from aw/ar_queue to avoid premature removal of requests
        # that are still needed for allocating downstream responses,
        # especially when the response cannot be accepted immediately.
        self.aw_check_queue: Queue[AxTask] = Queue[AxTask](2)
        self.ar_check_queue: Queue[AxTask] = Queue[AxTask](2)
        self.w_check_queue: Queue[WTask] = Queue[WTask](2)

    def resp_alloc(self):
        # Allocate B Channel response as long as the last beat fires.
        if self.io.w.fire() and bool(self.io.w.bits.last.value):
            assert not self.aw_queue.is_empty(), f"[{self.name} resp alloc error] Should be at least one aw task in aw queue!"

            self.b_queue.enq(
                BTask.random_gen(
                    aw = self.aw_queue.peek().flit,
                    alloc_cycle = self.dut.cycles.value.integer,
                    timeout_threshold = self.cfg.timeout_threshold,
                    label = self.name
                )
            )
            self.aw_queue.deq()

        if not self.ar_queue.is_empty():
            self.r_queue.enq(
                RTask.random_gen(
                    ar = self.ar_queue.peek().flit,
                    maxDataBytes = self.cfg.maxDataBytes,
                    busBytes = self.cfg.busBytes,
                    alloc_cycle = self.dut.cycles.value.integer,
                    timeout_threshold = self.cfg.timeout_threshold,
                    label = self.name
                )
            )
            self.ar_queue.deq()

    def set_rx_ready(self):
        """
        By default, as long as the AW/AR/R channel Queue has available slots
        it can always accept responses from the B/R channels,
        meaning the ready signals for the AW/AR/R channels are asserted high persistently.

        However, subclasses can implement customized handling,
        such as introducing delays or other logic modifications.
        """
        # Since elements in the aw/ar_check_queue are consumed by check() every clock cycle,
        # we expect the check_queue to perpetually maintain available slots.
        # Therefore, the assertion of the ready signals for the aw/ar channels
        # does not depend on whether the check_queue is full.
        self.io.aw.ready.value = int(not self.aw_queue.is_full())
        self.io.w .ready.value = int(not self.w_check_queue.is_full())
        self.io.ar.ready.value = int(not self.ar_queue.is_full())

    # TODO: decouple tx valid set from send.
    def send(self):
        if not self.r_queue.is_empty():
            self.io.r.send(self.r_queue.peek())
        else:
            self.io.r.valid.value = 0

        if not self.b_queue.is_empty():
            self.io.b.send(self.b_queue.peek())
        else:
            self.io.b.valid.value = 0

    def recv(self):
        if self.io.aw.fire():
            aw_task = AxTask.recv(
                bdl = self.io.aw,
                channel = Channel.AW,
                alloc_cycle = self.dut.cycles.value.integer,
                timeout_threshold = self.cfg.timeout_threshold,
                label = self.name
            )
            self.aw_queue.enq(aw_task)
            self.aw_check_queue.enq(aw_task)

        if self.io.w.fire():
            self.w_check_queue.enq(
                WTask.recv(
                    bdl = self.io.w,
                    alloc_cycle = self.dut.cycles.value.integer,
                    timeout_threshold = self.cfg.timeout_threshold,
                    label = self.name
                )
            )

        if self.io.ar.fire():
            ar_task = AxTask.recv(
                bdl = self.io.ar,
                channel = Channel.AR,
                alloc_cycle = self.dut.cycles.value.integer,
                timeout_threshold = self.cfg.timeout_threshold,
                label = self.name
            )
            self.ar_queue.enq(ar_task)
            self.ar_check_queue.enq(ar_task)

    def drive_phase(self):
        """
        Delta-cycle phase 1: drive output signals to the DUT.

        This function should be called immediately after the rising clock edge,
        in the first delta cycle of the simulation step. It performs:

          - Asserting ready signals for AW/AR/W channels based on queue availability.
          - Driving valid signals for B/R responses, if there are responses ready to send.
        """
        self.set_rx_ready()
        self.send()

    def sample_phase(self):
        """
        Delta-cycle phase 2: sample input signals from the DUT.

        This function should be called in the second delta cycle of the same clock cycle,
        after DUT outputs have settled. It performs:

          - Capturing AW/AR/W requests from the DUT and enqueuing them.
          - Allocating B/R responses based on completed AW/AR requests.

        This phase should always follow `drive_phase()` within the same simulation step.
        """
        self.recv()
        # Unlike master, resp_alloc() should be in sample_phase in slave,
        # because it depends on handshake signals to decide whether to allocate or not.
        self.resp_alloc()
