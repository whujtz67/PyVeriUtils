from enum import Enum

class Channel(Enum):
    AW = 0
    W  = 1
    B  = 2
    AR = 3
    R  = 4

    @staticmethod
    def is_addr_chnl(chnl) -> bool:
        return chnl in (Channel.AW, Channel.AR)

    @staticmethod
    def is_data_chnl(chnl) -> bool:
        return chnl in (Channel.W, Channel.R)

    @staticmethod
    def enum_to_str(chnl) -> str:
        return {
            Channel.AW: "AW",
            Channel.W : "W",
            Channel.B : "B",
            Channel.AR: "AR",
            Channel.R : "R"
        }[chnl]
    

class BurstType(Enum):
    # burst type
    FIXED = 0
    INCR  = 1
    WRAP  = 2

    @staticmethod
    def int_to_enum(int_i: int):
        return {
            0: BurstType.FIXED,
            1: BurstType.INCR,
            2: BurstType.WRAP
        }[int_i]


class RespType(Enum):
    # resp type
    OKAY    = 0
    EXOKAY  = 1
    SLAVERR = 2
    DECERR  = 3

    @staticmethod
    def int_to_enum(int_i: int):
        return {
            0: RespType.OKAY,
            1: RespType.EXOKAY,
            2: RespType.SLAVERR,
            3: RespType.DECERR
        }[int_i]

class TaskState(Enum):
    # Task State for sender
    NOTSENT  = 0
    INFLIGHT = 1
    FINISHED = 2

    # Task State for receiver
    RECEIVED      = 3 
    RECEIVING     = 4 # for w r
    RESP_SENT     = 5
    RESP_SENDING  = 6
    




