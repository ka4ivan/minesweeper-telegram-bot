from bot.db import SessionLocal
from bot.models.db.game import Game


class PostgresRepository:

    async def save_game_result(self, game):
        async with SessionLocal() as session:
            result = Game(
                user_id=game.user_id,
                mode=game.mode,
                width=game.width,
                height=game.height,
                mines=game.mines,
                status=game.status,
                duration=game.time_spent,
            )
            session.add(result)
            await session.commit()

    async def get_user_stats(self, user_id: int):
        async with SessionLocal() as session:
            return 0
