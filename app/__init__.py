# app/services.py - правильная версия
import os
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
from app.config import Config

# Часть 1: Работа с файлами
def save_image(file_bytes: bytes, user_id: int) -> str:
    """Сохраняет изображение на диск"""
    img = Image.open(BytesIO(file_bytes))
    path = Path(f"data/images/user_{user_id}.jpg")
    img.save(path)
    return str(path)

def save_audio(file_bytes: bytes, user_id: int) -> str:
    """Сохраняет аудиофайл"""
    path = Path(f"data/music/user_{user_id}.mp3")
    path.write_bytes(file_bytes)
    return str(path)

# Часть 2: Работа с API
def get_weather(city: str) -> dict:
    """Получает данные о погоде"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.OPENWEATHER_API_KEY}"
    return requests.get(url).json()