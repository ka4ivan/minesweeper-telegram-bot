from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class GameState:
    user_id: int
    mode: str
    width: int
    height: int
    mines: int
    board: List[List[str]] = field(default_factory=list)  # E=empty, M=mine, 1-8=number
    revealed: List[List[bool]] = field(default_factory=list)
    flags: List[List[bool]] = field(default_factory=list)
    is_over: bool = False
    won: Optional[bool] = None
