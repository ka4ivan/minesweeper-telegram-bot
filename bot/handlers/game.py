from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.game_keyboard import game_keyboard
from bot.dependencies import game_service
from bot.models.game_status import GameStatus
from bot.utils.i18n import _

router = Router()

@router.callback_query(F.data.startswith("game:"))
async def game_start_handler(query: CallbackQuery):
    mode = query.data.split(":")[1]
    game = await game_service.start_game(query.from_user.id, mode)

    await query.message.edit_text(
        f"Game {mode} started! Board {game.width}x{game.height}",
        reply_markup=game_keyboard(game)
    )


@router.callback_query(F.data.startswith("reveal:"))
async def reveal_cell_handler(query: CallbackQuery):
    __, game_id, x, y = query.data.split(":")
    x, y = int(x), int(y)

    result = await game_service.reveal_cell(
        user_id=query.from_user.id,
        game_id=game_id,
        x=x,
        y=y
    )
    game = result.game

    if not game:
        await query.answer(_("This game session is no longer active"), show_alert=False)
        return

    if game.status == GameStatus.END:
        await query.answer(_("Game over!"), show_alert=False)
        return

    if not result.changed:
        return

    if game.status in (GameStatus.WON, GameStatus.LOST):
        game.end_at = datetime.now(timezone.utc)

    if game.status == GameStatus.LOST:
        await query.message.edit_text(
            _("💥 You hit a mine! Game over!"),
            reply_markup=game_keyboard(game)
        )
    elif game.status == GameStatus.WON:
        await query.message.edit_text(
            _("🎉 You won!"),
            reply_markup=game_keyboard(game)
        )
    else:
        await query.message.edit_reply_markup(
            reply_markup=game_keyboard(game)
        )


@router.callback_query(F.data.startswith("mode:"))
async def switch_mode_handler(query: CallbackQuery):
    __, game_id = query.data.split(":")
    game = await game_service.toggle_mode(query.from_user.id, game_id)

    if not game.first_click_done:
        await query.answer(_("The game hasn’t started yet."), show_alert=False)
        return

    if not game:
        await query.answer(_("This game session is no longer active"), show_alert=False)
        return

    if game.status == GameStatus.END:
        await query.answer(_("Game over!"), show_alert=False)
        return

    await query.message.edit_reply_markup(
        reply_markup=game_keyboard(game)
    )
