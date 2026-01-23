from bot.models.cell_state import CellState
from bot.models.game_status import GameStatus
from uuid import uuid4
from pydantic import BaseModel, Field


class GameState(BaseModel):
    game_id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: int
    width: int
    height: int
    mines: int

    board: list[list[str]] = []
    cells: list[list[str]] = []
    status: str = GameStatus.PLAYING
    first_click_done: bool = False

    def generate_empty_board(self):
        self.board = [["E" for _ in range(self.width)] for _ in range(self.height)]
        self.cells = [[CellState.CLOSE for _ in range(self.width)] for _ in range(self.height)]

    def is_over(self) -> bool:
        return self.status in (GameStatus.WON, GameStatus.LOST)