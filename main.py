import asyncio
from aiogram import Bot, Dispatcher

from src.core.config import settings
from src.core.logger import setup_logger
from src.database.db import init_db
from src.handlers.user import user_router

async def main():
    setup_logger()
    
    await init_db()
    
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
    )
    
    dp = Dispatcher()
    
    dp.include_router(user_router)
    
    print("Бот запущен")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")