import random
from bot.models.game_state import GameState
from bot.repositories.redis_repository import RedisRepository

class GameService:
    def __init__(self, repo: RedisRepository):
        self.repo = repo

    async def start_game(self, user_id: int, mode: str) -> GameState:
        if mode == "beginner":
            width, height, mines = 5, 5, 5
        elif mode == "intermediate":
            width, height, mines = 7, 7, 10
        elif mode == "expert":
            width, height, mines = 8, 12, 20
        else:
            width, height, mines = 5, 5, 5  # default for MVP

        board = [["E" for _ in range(width)] for _ in range(height)]
        revealed = [[False]*width for _ in range(height)]
        flags = [[False]*width for _ in range(height)]

        # розставляємо міни
        cells = [(x, y) for x in range(height) for y in range(width)]
        for x, y in random.sample(cells, mines):
            board[x][y] = "M"

        game = GameState(
            user_id=user_id,
            mode=mode,
            width=width,
            height=height,
            mines=mines,
            board=board,
            revealed=revealed,
            flags=flags
        )

        await self.repo.save_game(game)
        return game

    async def reveal_cell(self, user_id: int, x: int, y: int) -> GameState:
        game = await self.repo.load_game(user_id)
        if not game or game.is_over:
            return game

        if game.revealed[x][y] or game.flags[x][y]:
            return game  # нічого не робимо

        if game.board[x][y] == "M":
            game.is_over = True
            game.won = False
        else:
            game.revealed[x][y] = True
            # Для MVP: без рекурсивного відкриття пустих
            # Можна додати flood fill пізніше

            # Перевірка перемоги
            safe_cells = sum(row.count(False) for row in game.revealed)
            if safe_cells == game.mines:
                game.is_over = True
                game.won = True

        await self.repo.save_game(game)
        return game
