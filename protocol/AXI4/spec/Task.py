from typing import Optional

from PyVeriUtils.utils.Common.Task import BaseTask
from PyVeriUtils.protocol.AXI4.spec.Encodings import Channel
from PyVeriUtils.protocol.AXI4.spec.DutBundle import AxBundle, WBundle, RBundle, BBundle
from PyVeriUtils.protocol.AXI4.spec.Flit import AxFlit, WBatch, RBatch, BFlit, WFlit, RFlit


class AxTask(BaseTask):
	def __init__(
			self,
			channel: Channel,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None,
	):
		super().__init__(
			name = "aw_task" if label is None else f"{label}_aw_task", 
			alloc_cycle = alloc_cycle, 
			timeout_threshold = timeout_threshold
		)
		self.channel = channel
		self.flit: Optional[AxFlit] = None

	@classmethod
	def customized(
			cls,
			flit: AxFlit,
			channel: Channel,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "AxTask":
		task = cls(channel, alloc_cycle, timeout_threshold, label)
		task.flit = flit

		return task

	@classmethod
	def recv(
			cls,
			bdl: AxBundle,
			channel: Channel,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "AxTask":
		task = cls(channel, alloc_cycle, timeout_threshold, label)
		task.flit = AxFlit.recv(bdl)

		return task

class WTask(BaseTask):
	def __init__(
			self,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None,
	):
		super().__init__(
			name = "w_task" if label is None else f"{label}_w_task",
			alloc_cycle = alloc_cycle,
			timeout_threshold = timeout_threshold
		)
		self.channel = Channel.W
		self.flit: Optional[WFlit] = None
		self.batch: Optional[WBatch] = None

	@classmethod
	def customized(
			cls,
			batch: WBatch,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "WTask":
		task = cls(alloc_cycle, timeout_threshold, label)
		task.batch = batch

		return task

	@classmethod
	def recv(
			cls,
			bdl: WBundle,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "WTask":
		task = cls(alloc_cycle, timeout_threshold, label)
		task.flit = WFlit.recv(bdl)

		return task

class RTask(BaseTask):
	def __init__(
			self,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None,
	):
		super().__init__(
			name = "r_task" if label is None else f"{label}_r_task",
			alloc_cycle = alloc_cycle,
			timeout_threshold = timeout_threshold
		)
		self.channel = Channel.R
		self.flit: Optional[RFlit] = None
		self.batch: Optional[RBatch] = None

	@classmethod
	def customized(
		cls,
		batch: RBatch,
		alloc_cycle: int,
		timeout_threshold: int = 10000,
		label: Optional[str] = None,
	) -> "RTask":
		task = cls(
			alloc_cycle = alloc_cycle,
			timeout_threshold = timeout_threshold,
			label = label,
		)
		task.batch = batch

		return task

	@classmethod
	def recv(
			cls,
			bdl: RBundle,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "RTask":
		task = cls(alloc_cycle, timeout_threshold, label)
		task.flit = RFlit.recv(bdl)

		return task

	@classmethod
	def random_gen(
			cls,
			ar: AxFlit,
			maxDataBytes: int,
			busSize: int,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "RTask":
		task = cls(alloc_cycle, timeout_threshold, label)
		task.batch = RBatch.random_gen(ar, maxDataBytes, busSize)

		return task

class BTask(BaseTask):
	def __init__(
			self,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None,
	):
		super().__init__(
			name = "b_task" if label is None else f"{label}_b_task",
			alloc_cycle = alloc_cycle,
			timeout_threshold = timeout_threshold
		)
		self.channel = Channel.B
		self.flit: Optional[BFlit] = None

	@classmethod
	def customized(
		cls,
		flit: BFlit,
		alloc_cycle: int,
		timeout_threshold: int = 10000,
		label: Optional[str] = None,
	) -> "BTask":
		task = cls(
			alloc_cycle = alloc_cycle,
			timeout_threshold = timeout_threshold,
			label = label,
		)
		task.flit = flit
		return task

	@classmethod
	def recv(
			cls,
			bdl: BBundle,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "BTask":
		task = cls(alloc_cycle, timeout_threshold, label)
		task.flit = BFlit.recv(bdl)

		return task

	@classmethod
	def random_gen(
			cls,
			aw: AxFlit,
			alloc_cycle: int,
			timeout_threshold: int = 10000,
			label: Optional[str] = None
	) -> "BTask":
		task = cls(alloc_cycle, timeout_threshold, label)
		task.flit = BFlit.random_gen(aw)

		return task

