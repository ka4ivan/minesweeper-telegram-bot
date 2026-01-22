from pydantic import BaseModel

from bot.models.cell_state import CellState
from bot.models.game_status import GameStatus


class GameState(BaseModel):
    user_id: int
    width: int
    height: int
    mines: int

    board: list[list[str]] = []          # "E" | "M"
    cells: list[list[str]] = []          # CellState.*
    status: str = GameStatus.PLAYING
    first_click_done: bool = False

    def generate_empty_board(self):
        self.board = [["E" for _ in range(self.width)] for _ in range(self.height)]
        self.cells = [[CellState.CLOSE for _ in range(self.width)] for _ in range(self.height)]

    def is_over(self) -> bool:
        return self.status in (GameStatus.WON, GameStatus.LOST)