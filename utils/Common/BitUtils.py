from typing import List

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
    def slice_by_stride(data: int, total_bits: int, stride: int) -> List[int]:
        """
        Splits `data` from LSB to MSB into chunks of `stride` bits.

        Args:
            data (int): The input integer to split.
            total_bits (int): The total number of meaningful bits in `data`.
            stride (int): The bit-width of each chunk (stride length).

        Returns:
            List[int]: A list of integers, each `stride` bits wide, LSB-first.
        """
        assert total_bits % stride == 0, "total_bits must be divisible by stride"
        result: List[int] = []

        for i in range(total_bits // stride):
            shift = i * stride
            mask = (1 << stride) - 1
            chunk = (data >> shift) & mask
            result.append(chunk)

        return result

    @staticmethod
    def split_into_bits(data: int, total_bits: int) -> list[int]:
        return [(data >> i) & 1 for i in range(total_bits)]

    @staticmethod
    def apply_byte_enable(data: int, be: int) -> int:
        return data & BitUtils.be_to_bit_en(be)

    @staticmethod
    def apply_nibble_enable(data: int, nbe: int) -> int:
        return data & BitUtils.nbe_to_bit_en(nbe)