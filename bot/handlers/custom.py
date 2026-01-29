from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.models.custom_settings import CustomSettings
from bot.dependencies import game_service
from bot.utils.i18n import _

router = Router()


@router.message(Command("custom"))
async def set_custom_mode(message: Message):
    parts = message.text.split()

    if len(parts) != 4:
        await message.answer(_("Usage:\n<code>/custom 8 10 30</code> \n\nSetting:\n/custom <i>width</i> <i>height</i> <i>mines</i>"))

        return None

    try:
        width, height, mines = map(int, parts[1:])
    except ValueError:
        return await message.answer(_("Numbers only: /custom 8 10 30"))

    if width < 5 or height < 5:
        return await message.answer(_("Board too small (min 5x5)"))

    if mines >= width * height - 9:
        return await message.answer(_("Too many mines for this board size"))

    settings = CustomSettings(width=width, height=height, mines=mines)
    await game_service.save_custom_settings(message.from_user.id, settings)

    await message.answer(
        _(
            f"✅ Custom mode saved: {width}x{height}, {mines} mines\n"
            f"Now press Custom in start menu."
        )
    )

    return None
