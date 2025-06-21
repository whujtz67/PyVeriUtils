from typing import Generic, TypeVar, Optional

T     = TypeVar('T')
T_IN  = TypeVar('T_IN')
T_OUT = TypeVar('T_OUT')

# In the verification environment, simulation components may need to communicate with each other.
# To ensure simplicity in their connections, we adopted a hardware module approach by adding I/O ports to them.
# Since these are software-based virtual modules, their I/O ports are referred to as SoftwareIO (sio)

class sValidIO(Generic[T]):
    def __init__(self):
        self.bits: Optional[T] = None
        self.valid: bool = False

    def fire(self) -> bool:
        return self.valid

    def set_and_validate(self, bits: T) -> None:
        self.bits = bits
        self.valid = True

    def clear(self) -> None:
        self.bits = None
        self.valid = False

class sDecoupledIO(sValidIO[T]):
    def __init__(self):
        super().__init__()
        self.ready = False

    def fire(self) -> bool:
        return self.valid and self.ready

    def clear(self):
        self.bits = None
        self.valid = False
        self.ready = False

class sCommonIO(Generic[T_IN, T_OUT]):
    def __init__(self):
        self.i: Optional[T_IN]  = None
        self.o: Optional[T_OUT] = None

class Flipped:
    def __init__(self, sio: sCommonIO[T_IN, T_OUT]):
        super().__init__()
        self.i = sio.o
        self.o = sio.i