from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.start_keyboard import start_keyboard
from bot.utils.i18n import _

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        text=(_("👋 Welcome!\n\nPress the button to start the game.")),
        reply_markup=start_keyboard(),
    )