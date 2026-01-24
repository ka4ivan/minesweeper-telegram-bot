from .start import router as start_router
from .game import router as game_router
from .custom import router as custom_router

__all__ = [
    "start_router",
    "game_router",
    "custom_router",
]