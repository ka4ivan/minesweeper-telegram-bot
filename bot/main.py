import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.dependencies import redis
from bot.middlewares.i18n import I18nMiddleware
from bot.handlers.start import router as start_router
from bot.handlers.game import router as game_router
from bot.handlers.custom import router as custom_router
from bot.models.db.game_result import Base
from bot.db import engine

async def main():
    logging.basicConfig(level=logging.INFO)

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    dp.message.middleware(I18nMiddleware())
    dp.callback_query.middleware(I18nMiddleware())

    dp.include_router(start_router)
    dp.include_router(custom_router)
    dp.include_router(game_router)

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    logging.info("🚀 Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await redis.close()

if __name__ == "__main__":
    asyncio.run(main())
