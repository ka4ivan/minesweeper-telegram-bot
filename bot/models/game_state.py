from datetime import datetime, timezone

from bot.models.cell_state import CellState
from bot.models.game_mode_action import GameAction
from bot.models.game_status import GameStatus
from uuid import uuid4
from pydantic import BaseModel, Field


class GameState(BaseModel):
    game_id: str = Field(default_factory=lambda: uuid4().hex)
    user_id: int
    mode: str
    width: int
    height: int
    mines: int

    board: list[list[str]] = []
    cells: list[list[str]] = []
    status: str = GameStatus.PLAYING
    first_click_done: bool = False
    action_mode: str = GameAction.REVEAL

    start_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_at: datetime | None = None

    def generate_empty_board(self):
        self.board = [["E" for _ in range(self.width)] for _ in range(self.height)]
        self.cells = [[CellState.CLOSE for _ in range(self.width)] for _ in range(self.height)]

    def is_over(self) -> bool:
        return self.status in (GameStatus.WON, GameStatus.LOST)

    @property
    def remaining_mines(self) -> int:
        flags = sum(
            1
            for row in self.cells
            for cell in row
            if cell == CellState.FLAG
        )
        return self.mines - flags

    @property
    def time_spent(self) -> int:
        if not self.first_click_done:
            return 0
        now = datetime.now(timezone.utc)
        end_at = self.end_at or now
        return int((end_at - self.start_at).total_seconds())