from typing import List, Optional

class SignalBinding:
    """
        The 'signalBinding' module decouples signals from the DUT and binds them to instances of a Python class.
        The rationale for this approach over directly accessing/assigning signals via dut.xxx.xxx (recommended by Cocotb’s official guidelines) is to improve code reusability.

        For example, if there are multiple Axi Master Bundles with identical structures but different numbering,
        using Cocotb's official approach would require individual assignments for each Bundle.
        However, by decoupling and binding signals, a single function can handle all cases by passing the decoupled signal instances as arguments.
    """
    @staticmethod
    def hierarchical_path(suffix: str, prefix: Optional[str] = None, hierarchy: Optional[str] = None) -> str:
        prefix_str = f"{prefix}_" if prefix is not None else ""
        hierar_str = f"{hierarchy}." if hierarchy is not None else ""

        return f"{hierar_str}{prefix_str}{suffix}"

class DutSignal(SignalBinding):
    def __init__(
            self,
            dut ,
            suffix   : str,
            prefix   : Optional[str] = None,
            hierarchy: Optional[str] = None

    ) -> None:
        path: str = self.hierarchical_path(suffix, prefix, hierarchy)

        print(f"[Signal Binding] {path}")

        setattr(self, suffix, getattr(dut, path))

class DutBundle(SignalBinding):
    def __init__(
            self,
            dut,
            fields: List[str],
            prefix: Optional[str] = None,
            hierarchy: Optional[str] = None
    ) -> None:
        for field in fields:
            path: str = self.hierarchical_path(field, prefix, hierarchy)

            print(f"[Signal Binding] {path}")

            setattr(self, field, getattr(dut, path))

        # TODO: rewrite <= and >=

# The same bundle structure with DecoupledIO in chisel
class DecoupledIO(SignalBinding):
    """
        The DecoupledIO class in Chisel is a utility for implementing ready-valid handshake interfaces.

        [Structure]:

        valid: Signals data availability from producer
        ready: Signals consumer readiness
        bits : Carries payload data

        full hierarchical path of DecoupledIO Signals:
            dut.<hierarchy>.<prefix>_bits_<fields>
            dut.<hierarchy>.<prefix>_valid
            dut.<hierarchy>.<prefix>_ready
    """
    def __init__(
            self,
            dut,
            fields   : List[str],
            prefix   : str,                   # Should always have a prefix for DecoupledIO bundle.
            hierarchy: Optional[str] = None,
            has_bits : bool = True            # To control whether we have "bits" in signal name.
    ) -> None:
        self.bits  = DutBundle(dut, fields, prefix = f"{prefix}_bits" if has_bits else prefix, hierarchy = hierarchy)
        self.valid = getattr(dut, self.hierarchical_path(
            suffix    = "valid",
            prefix    = prefix,
            hierarchy = hierarchy
        ))
        self.ready = getattr(dut, self.hierarchical_path(
            suffix    = "ready",
            prefix    = prefix,
            hierarchy = hierarchy
        ))

    def fire(self) -> bool:
        return bool(self.valid.value and self.ready.value)

    def is_ready(self) -> bool:
        return bool(self.ready.value)