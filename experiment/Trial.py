import math
from enum import Enum
class Trial:
    def __init__(self, id, sequence):
        self.id = id
        self.sequence = sequence


class Flag(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4 
    F = 5 