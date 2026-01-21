from random import random, randint

from bot.keyboards.game_keyboard import count_adjacent_mines
from bot.repositories.redis_repository import RedisRepository
from bot.models.game_state import GameState

class GameService:
    def __init__(self, repo: RedisRepository):
        self.repo = repo

    async def start_game(self, user_id: int, mode: str) -> GameState:
        if mode == "beginner":
            width, height, mines = 5, 5, 5
        elif mode == "intermediate":
            width, height, mines = 7, 7, 10
        elif mode == "expert":
            width, height, mines = 12, 8, 20
        else:
            width, height, mines = 5, 5, 5

        game = GameState(user_id=user_id, width=width, height=height, mines=mines)
        game.generate_empty_board()
        await self.repo.save_game(game)
        return game

    async def reveal_cell(self, user_id: int, x: int, y: int) -> GameState:
        game = await self.repo.load_game(user_id)
        if not game or game.status != "playing":
            game.status = "end"
            return game

        if game.revealed[x][y]:
            return game

        if not game.first_click_done:
            self._place_mines_safe_first_click(game, x, y)
            game.first_click_done = True

        if game.board[x][y] == "M":
            game.revealed[x][y] = True
            game.status = "lost"
            for i in range(game.height):
                for j in range(game.width):
                    if game.board[i][j] == "M":
                        game.revealed[i][j] = True
            await self.repo.save_game(game)
            return game

        self._flood_fill(game, x, y)

        if self._check_win(game):
            game.status = "won"

        await self.repo.save_game(game)
        return game

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
        if game.revealed[x][y]:
            return

        game.revealed[x][y] = True
        if count_adjacent_mines(game.board, x, y) > 0:
            return

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < game.height and 0 <= ny < game.width:
                    if not game.revealed[nx][ny] and game.board[nx][ny] != "M":
                        self._flood_fill(game, nx, ny)

    def _check_win(self, game: GameState) -> bool:
        for i in range(game.height):
            for j in range(game.width):
                if game.board[i][j] != "M" and not game.revealed[i][j]:
                    return False
        return True
