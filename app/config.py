import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")