"""Entrypoint: wires everything together and starts long polling."""
from __future__ import annotations

import asyncio
import logging

from aiogram.types import ErrorEvent

from handlers import main_router
from loader import bot, db, dp, setup_middlewares
from utils.logger import setup_logging

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    await db.connect()
    logger.info("Baza ulandi: %s", db.path)


async def on_shutdown() -> None:
    await db.close()
    await bot.session.close()
    logger.info("Bot to'xtatildi.")


def register_error_handler() -> None:
    @dp.errors()
    async def global_error_handler(event: ErrorEvent) -> bool:
        logger.exception(
            "Update ishlov berishda xatolik: %s | update=%s", event.exception, event.update
        )
        return True


async def main() -> None:
    setup_logging()
    setup_middlewares()
    register_error_handler()

    dp.include_router(main_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger(__name__).info("Bot foydalanuvchi tomonidan to'xtatildi.")
