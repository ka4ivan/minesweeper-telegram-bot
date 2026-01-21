from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

def game_keyboard(game, exploded: tuple[int,int] | None = None) -> InlineKeyboardMarkup:
    inline_keyboard = []

    for x in range(game.height):
        row = []
        for y in range(game.width):
            if game.revealed[x][y]:
                cell = game.board[x][y]

                if exploded and (x, y) == exploded:
                    text = "💥"
                elif cell == "M":
                    text = "💣"
                elif cell == "E":
                    mines_count = count_adjacent_mines(game.board, x, y)
                    text = str(mines_count) if mines_count > 0 else "⬜"
                else:
                    text = cell
            elif game.flags[x][y]:
                text = "🚩"
            else:
                text = "▪️"

            callback_data = f"reveal:{x}:{y}"
            row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
