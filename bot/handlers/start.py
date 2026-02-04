from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.db import AsyncSessionLocal
from bot.keyboards.start_keyboard import start_keyboard
from bot.repositories.user_repository import UserRepository
from bot.services.user_service import UserService
from bot.utils.i18n import _

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user_service = UserService(UserRepository(session))
        await user_service.get_or_create(message.from_user)

    await message.answer(
        text=(_("👋 Welcome!\n\nPress the button to start the game.")),
        reply_markup=start_keyboard(),
    )