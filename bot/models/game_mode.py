from enum import Enum

class GameMode(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
    CUSTOM = "custom"
