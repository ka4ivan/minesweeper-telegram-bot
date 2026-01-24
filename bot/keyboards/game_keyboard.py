from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.emoji import CELL_EMPTY, CELL_STATE_EMOJI, GAME_STATUS_EMOJI
from bot.models.cell_state import CellState
from bot.models.game_mode_action import GameAction
from bot.utils.i18n import _


def count_adjacent_mines(board, x, y):
    height = len(board)
    width = len(board[0])
    count = 0

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width:
                if board[nx][ny] == "M":
                    count += 1
    return count


def game_keyboard(game) -> InlineKeyboardMarkup:
    keyboard = []

    # stats
    minutes, seconds = divmod(game.time_spent, 60)
    timer_text = f"{minutes:02d}:{seconds:02d}"

    keyboard.append([
        InlineKeyboardButton(
            text=_("💣 {count}").format(count=game.remaining_mines),
            callback_data="noop"
        ),
        InlineKeyboardButton(
            text=GAME_STATUS_EMOJI[game.status],
            callback_data="game:" + game.mode
        ),
        InlineKeyboardButton(
            text=_("🕔 {time}").format(time=timer_text),
            callback_data="noop"
        )
    ])

    # game
    for x in range(game.height):
        row = []
        for y in range(game.width):
            state = game.cells[x][y]

            if state == CellState.OPEN:
                count = count_adjacent_mines(game.board, x, y)
                text = str(count) if count > 0 else CELL_EMPTY
            else:
                text = CELL_STATE_EMOJI[state]

            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"reveal:{game.game_id}:{x}:{y}"
                )
            )
        keyboard.append(row)

    # settings
    mode_text = _("Mode: 🚩 Flag") if game.action_mode == GameAction.FLAG else _("Mode: 🧭 Reveal")

    keyboard.append([
        InlineKeyboardButton(
            text=mode_text,
            callback_data=f"mode:{game.game_id}"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
