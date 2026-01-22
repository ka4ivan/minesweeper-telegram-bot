from enum import Enum

class CellState(str, Enum):
    CLOSE = "close"
    OPEN = "open"
    MINE = "mine"
    FLAG = "flag"
    EXPLODE = "explode"
