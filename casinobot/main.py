import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import Settings
from fluent_loader import get_fluent_localization
from ui_commands import set_bot_commands
from Middlewares.throttling import ThrottlingMiddleware
from Handlers import userHandlers, spinHandler

async def main():
    logging.basicConfig(level=logging.INFO)
    config = Settings()

    storage = MemoryStorage()

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    l10n = get_fluent_localization(config.bot_language)

    dp = Dispatcher(storage=storage, l10n=l10n, config=config)

    dp.message.filter(F.chat.type == "private")

    dp.include_router(userHandlers.router)
    dp.include_router(spinHandler.router)

    dp.message.middleware(ThrottlingMiddleware(config.throttle_time_spin, config.throttle_time_other))

    await set_bot_commands(bot, l10n)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())