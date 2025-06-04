
class BitUtils:
    @staticmethod
    def be_to_bit_en(be: int) -> int:
        bit_en = 0
        for i in range(be.bit_count()):
            byte_flag = (be >> i) & 0x1
            byte_mask = 0xFF if bool(byte_flag) else 0

            bit_en |= byte_mask << (8 * i)

        return bit_en

    @staticmethod
    def nbe_to_bit_en(be: int) -> int:
        bit_en = 0
        for i in range(be.bit_count()):
            byte_flag = (be >> i) & 0x1
            byte_mask = 0xF if bool(byte_flag) else 0

            bit_en |= byte_mask << (4 * i)

        return bit_en

    @staticmethod
    def apply_byte_enable(data: int, be: int) -> int:
        return data & BitUtils.be_to_bit_en(be)

    @staticmethod
    def apply_nibble_enable(data: int, nbe: int) -> int:
        return data & BitUtils.nbe_to_bit_en(nbe)