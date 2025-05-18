import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.database import SessionLocal, init_db
from app.handlers import register_handlers
from dotenv import load_dotenv

load_dotenv()

# Инициализация бота
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Инициализация БД
init_db()

# Регистрация обработчиков
register_handlers(dp)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)