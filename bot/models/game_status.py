from enum import Enum

class GameStatus(str, Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
    END = "end"
