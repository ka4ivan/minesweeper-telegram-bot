from bot.models.cell_state import CellState
from bot.models.game_status import GameStatus

CELL_STATE_EMOJI = {
    CellState.CLOSE: "◾️",
    CellState.FLAG: "❤️", # TODO 🚩
    CellState.MISTAKE: "🚫",
    CellState.MINE: "💣",
    CellState.EXPLODE: "💥",
}

CELL_EMPTY = "⬜️"

GAME_STATUS_EMOJI = {
    GameStatus.PLAYING: "🙂",
    GameStatus.WON: "😎",
    GameStatus.LOST: "😵",
}
