from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models.game_mode import GameMode
from bot.utils.i18n import _

def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("🎮 5x5"),
                    callback_data="game:" + GameMode.BEGINNER,
                ),
                InlineKeyboardButton(
                    text=_("🎮 7x7"),
                    callback_data="game:" + GameMode.BEGINNER,
                ),
                InlineKeyboardButton(
                    text=_("🎮 8x12"),
                    callback_data="game:" + GameMode.BEGINNER,
                )
            ],
        [
            InlineKeyboardButton(
                text=_("⚙️ Custom"),
                callback_data="game:" + GameMode.BEGINNER,
            ),
        ]
        ]
    )