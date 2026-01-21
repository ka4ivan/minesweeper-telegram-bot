from redis.asyncio import Redis
from bot.repositories.redis_repository import RedisRepository
from bot.services.game_service import GameService

redis = Redis(host="redis", port=6379, decode_responses=True)

redis_repo = RedisRepository(redis)

game_service = GameService(repo=redis_repo)
