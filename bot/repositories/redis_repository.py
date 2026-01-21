import json
from redis.asyncio import Redis
from bot.models.game_state import GameState

class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_game(self, game: GameState):
        key = f"game:{game.user_id}"
        await self.redis.set(key, json.dumps(game.__dict__), ex=3600)

    async def load_game(self, user_id: int) -> GameState | None:
        key = f"game:{user_id}"
        data = await self.redis.get(key)
        if not data:
            return None
        return GameState(**json.loads(data))

    async def delete_game(self, user_id: int):
        await self.redis.delete(f"game:{user_id}")
