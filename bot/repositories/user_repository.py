from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.db.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int, username: str | None, firstname: str | None) -> User:
        user = User(
            telegram_id=telegram_id,
            username=username,
            firstname=firstname,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
