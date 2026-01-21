from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.dependencies import game_service

router = Router()

@router.callback_query(F.data.startswith("game:"))
async def game_start_handler(query: CallbackQuery):
    mode = query.data.split(":")[1]
    game = await game_service.start_game(query.from_user.id, mode)

    await query.message.edit_text(
        f"Game {mode} started! Board {game.width}x{game.height}",
        reply_markup=None
    )
