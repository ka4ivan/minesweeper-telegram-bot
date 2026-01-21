from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.game_keyboard import game_keyboard
from bot.dependencies import game_service
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
    __, x, y = query.data.split(":")
    x, y = int(x), int(y)

    game = await game_service.reveal_cell(query.from_user.id, x, y)
    print(game.status)
    if game.status == "end":
        await query.answer(_("Game over!"), show_alert=False)
        return

    if game.status == "lost":
        await query.message.edit_text(
            _("💥 You hit a mine! Game over!"),
            reply_markup=game_keyboard(game, exploded=(x, y))
        )
    elif game.status == "won":
        await query.message.edit_text(
            _("🎉 You won!"),
            reply_markup=game_keyboard(game)
        )
    else:
        await query.message.edit_reply_markup(
            reply_markup=game_keyboard(game)
        )
