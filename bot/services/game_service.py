from datetime import datetime, timezone
from random import randint

from bot.keyboards.game_keyboard import count_adjacent_mines
from bot.models.cell_state import CellState
from bot.models.custom_settings import CustomSettings
from bot.models.game_mode import GameMode
from bot.models.game_mode_action import GameAction
from bot.models.game_status import GameStatus
from bot.models.reveal_result import RevealResult
from bot.repositories.redis_repository import RedisRepository
from bot.models.game_state import GameState

class GameService:
    def __init__(self, repo: RedisRepository):
        self.repo = repo

    async def start_game(self, user_id: int, mode: str) -> GameState:
        if mode == GameMode.BEGINNER:
            width, height, mines = 5, 5, 5
        elif mode == GameMode.INTERMEDIATE:
            width, height, mines = 7, 7, 7 # TODO 10
        elif mode == GameMode.EXPERT:
            width, height, mines = 8, 12, 12 # TODO 25
        elif mode == GameMode.CUSTOM:
            settings = await self.repo.load_custom_settings(user_id)

            if not settings:
                width, height, mines = 7, 7, 10
            else:
                width, height, mines = settings.width, settings.height, settings.mines
        else:
            width, height, mines = 5, 5, 5

        game = GameState(user_id=user_id, width=width, height=height, mines=mines, mode=mode)
        game.generate_empty_board()
        await self.repo.save_game(game)
        return game

    async def reveal_cell(self, user_id: int, game_id: str, x: int, y: int) -> RevealResult:
        game = await self.repo.load_game(user_id, game_id)
        if not game:
            return RevealResult(None, False)

        if game.status != GameStatus.PLAYING:
            game.status = GameStatus.END
            return RevealResult(game, False)

        if game.action_mode == GameAction.FLAG:
            return await self._toggle_flag(game, x, y)

        return await self._reveal(game, x, y)

    async def save_custom_settings(self, user_id: int, settings: CustomSettings):
        await self.repo.save_custom_settings(user_id, settings)

    async def toggle_mode(self, user_id: int, game_id: str) -> GameState:
        game = await self.repo.load_game(user_id, game_id)
        if not game:
            return None

        if game.status != GameStatus.PLAYING:
            game.status = GameStatus.END
            return game

        game.action_mode = (
            GameAction.FLAG if game.action_mode == GameAction.REVEAL else GameAction.REVEAL
        )

        await self.repo.save_game(game)
        return game

    async def _reveal(self, game: GameState, x: int, y: int) -> RevealResult:
        if game.cells[x][y] == CellState.FLAG:
            return RevealResult(game, False)

        prev_state = game.cells[x][y]

        if prev_state != CellState.CLOSE:
            return RevealResult(game, False)

        if not game.first_click_done:
            self._place_mines_safe_first_click(game, x, y)
            game.first_click_done = True
            game.start_at = datetime.now(timezone.utc)

        if game.board[x][y] == "M":
            game.cells[x][y] = CellState.EXPLODE
            game.status = GameStatus.LOST

            for i in range(game.height):
                for j in range(game.width):
                    if game.board[i][j] == "M" and game.cells[i][j] != CellState.EXPLODE and game.cells[i][j] != CellState.FLAG:
                        game.cells[i][j] = CellState.MINE
                    if game.board[i][j] != "M" and game.cells[i][j] == CellState.FLAG:
                        game.cells[i][j] = CellState.MISTAKE

            await self.repo.save_game(game)
            return RevealResult(game, True)

        self._flood_fill(game, x, y)

        if self._check_win(game):
            game.status = GameStatus.WON

        await self.repo.save_game(game)

        changed = prev_state != game.cells[x][y]
        return RevealResult(game, changed)

    async def _toggle_flag(self, game: GameState, x: int, y: int) -> RevealResult:
        state = game.cells[x][y]

        if state == CellState.OPEN:
            return RevealResult(game, False)

        if not game.first_click_done:
            return RevealResult(game, False)

        if state != CellState.FLAG and game.remaining_mines <= 0:
            return RevealResult(game, False)

        game.cells[x][y] = (
            CellState.CLOSE if state == CellState.FLAG else CellState.FLAG
        )

        await self.repo.save_game(game)
        return RevealResult(game, True)

    def _place_mines_safe_first_click(self, game: GameState, safe_x: int, safe_y: int):
        safe_cells = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = safe_x + dx, safe_y + dy
                if 0 <= nx < game.height and 0 <= ny < game.width:
                    safe_cells.add((nx, ny))

        mines_placed = 0
        while mines_placed < game.mines:
            x = randint(0, game.height - 1)
            y = randint(0, game.width - 1)
            if (x, y) in safe_cells:
                continue
            if game.board[x][y] != "M":
                game.board[x][y] = "M"
                mines_placed += 1

    def _flood_fill(self, game: GameState, x: int, y: int):
        if game.cells[x][y] != CellState.CLOSE:
            return

        game.cells[x][y] = CellState.OPEN

        if count_adjacent_mines(game.board, x, y) > 0:
            return

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < game.height and 0 <= ny < game.width:
                    self._flood_fill(game, nx, ny)

    def _check_win(self, game: GameState) -> bool:
        for i in range(game.height):
            for j in range(game.width):
                if game.board[i][j] != "M" and game.cells[i][j] != CellState.OPEN:
                    return False

        for i in range(game.height):
            for j in range(game.width):
                if game.board[i][j] == "M" and game.cells[i][j] != CellState.FLAG:
                    game.cells[i][j] = CellState.FLAG

        return True
