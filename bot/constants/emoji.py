from bot.models.cell_state import CellState

CELL_STATE_EMOJI = {
    CellState.CLOSE: "◾️",
    CellState.FLAG: "🚩",
    CellState.MISTAKE: "🚫",
    CellState.MINE: "💣",
    CellState.EXPLODE: "💥",
}

CELL_EMPTY = "⬜️"
