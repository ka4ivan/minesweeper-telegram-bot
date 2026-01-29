from bot.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_or_create(self, telegram_user) :
        user = await self.repo.get_by_telegram_id(telegram_user.id)

        if user:
            return user

        return await self.repo.create(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            firstname=telegram_user.first_name,
        )