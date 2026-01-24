from redis.asyncio import Redis

from bot.models.custom_settings import CustomSettings
from bot.models.game_state import GameState

CUSTOM_SETTINGS_KEY = "settings:custom:{user_id}"

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

    async def save_custom_settings(self, user_id: int, settings: CustomSettings):
        await self.redis.set(
            CUSTOM_SETTINGS_KEY.format(user_id=user_id),
            settings.model_dump_json()
        )

    async def load_custom_settings(self, user_id: int) -> CustomSettings | None:
        data = await self.redis.get(CUSTOM_SETTINGS_KEY.format(user_id=user_id))
        return CustomSettings.model_validate_json(data) if data else None
