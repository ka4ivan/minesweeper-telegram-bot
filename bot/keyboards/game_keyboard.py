from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models.cell_state import CellState


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

    for x in range(game.height):
        row = []
        for y in range(game.width):
            state = game.cells[x][y]

            if state == CellState.CLOSE:
                text = "▪️"
            elif state == CellState.FLAG:
                text = "🚩"
            elif state == CellState.MINE:
                text = "💣"
            elif state == CellState.EXPLODE:
                text = "💥"
            else:  # OPEN
                count = count_adjacent_mines(game.board, x, y)
                text = str(count) if count > 0 else "⬜"

            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"reveal:{x}:{y}"
                )
            )
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
