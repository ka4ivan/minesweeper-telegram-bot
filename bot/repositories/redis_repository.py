from redis.asyncio import Redis
from bot.models.game_state import GameState

class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_game(self, game: GameState):
        key = f"game:{game.user_id}:{game.game_id}"
        await self.redis.set(key, game.model_dump_json())

    async def load_game(self, user_id: int, game_id: str) -> GameState | None:
        key = f"game:{user_id}:{game_id}"
        data = await self.redis.get(key)
        return GameState.model_validate_json(data) if data else None

    async def delete_game(self, user_id: int):
        await self.redis.delete(f"game:{user_id}")
