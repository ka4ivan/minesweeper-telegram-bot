from redis.asyncio import Redis
from bot.repositories.redis_repository import RedisRepository
from bot.services.game_service import GameService
import os

redis = Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), decode_responses=True)

redis_repo = RedisRepository(redis)

game_service = GameService(repo=redis_repo)
