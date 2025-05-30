from db_helper import DBHelper
from tb_config import TBConfig
from spec.Flit import *

class AXI4_DB_Helper(DBHelper):
	def __init__(self, cfg: TBConfig) -> None:
		super().__init__(cfg)

	def aw_save_db(self, cycles, name, bits: AW_Flit):
		self.save_db(cycles, name, "AW", bits.id, bits.addr, bits.len, bits.size)

	def w_save_db(self, cycles, name, bits: W_Flit):
		self.save_db(cycles, name, "W", bits.id, data=bits.data, strb=bits.strb, last=bits.last)

	def b_save_db(self, cycles, name, bits: B_Flit):
		self.save_db(cycles, name, "B", bits.id)

	def ar_save_db(self, cycles, name, bits: AR_Flit):
		self.save_db(cycles, name, "AR", bits.id, bits.addr, bits.len, bits.size)

	def r_save_db(self, cycles, name, bits: R_Flit):
		self.save_db(cycles, name, "R", bits.id, data=bits.data, last=bits.last)