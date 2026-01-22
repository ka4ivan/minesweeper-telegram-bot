from pydantic import BaseModel

from bot.models.game_status import GameStatus


class GameState(BaseModel):
    user_id: int
    width: int
    height: int
    mines: int
    board: list[list[str]] = []
    revealed: list[list[bool]] = []
    flags: list[list[bool]] = []
    status: str = GameStatus.PLAYING
    first_click_done: bool = False

    def generate_empty_board(self):
        self.board = [["E" for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.flags = [[False for _ in range(self.width)] for _ in range(self.height)]
