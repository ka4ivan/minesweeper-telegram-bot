from dataclasses import dataclass
from bot.models.game_state import GameState

@dataclass
class RevealResult:
    game: GameState
    changed: bool
