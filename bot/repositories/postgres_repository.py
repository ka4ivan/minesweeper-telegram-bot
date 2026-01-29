from sqlalchemy import select, func, Integer
from bot.db import SessionLocal
from bot.models.db.game_result import GameResult

from bot.models.game_status import GameStatus


class PostgresRepository:

    async def save_game_result(self, game):
        async with SessionLocal() as session:
            result = GameResult(
                user_id=game.user_id,
                mode=game.mode,
                width=game.width,
                height=game.height,
                mines=game.mines,
                won=game.status == GameStatus.WON,
                duration=game.time_spent,
            )
            session.add(result)
            await session.commit()

    async def get_user_stats(self, user_id: int):
        async with SessionLocal() as session:
            stmt = select(
                func.count().label("games"),
                func.sum(GameResult.won.cast(Integer)).label("wins")
            ).where(GameResult.user_id == user_id)

            result = await session.execute(stmt)
            return result.first()
