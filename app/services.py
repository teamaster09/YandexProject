import time
import secrets
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
from app.config import Config
OPENWEATHER_API_KEY = Config.OPENWEATHER_API_KEY


def save_image(file_bytes: bytes, user_id: int) -> str:
    """Сохраняет изображение с уникальным именем"""
    img = Image.open(BytesIO(file_bytes))

    # Генерируем уникальное имя файла: user_123_ timestamp_random.jpg
    timestamp = int(time.time())
    random_str = secrets.token_hex(3)  # 6 случайных символов
    filename = f"user_{user_id}_{timestamp}_{random_str}.jpg"

    path = Path("data/images") / filename
    img.save(path)

    return str(path)


def save_audio(file_bytes: bytes, user_id: int) -> str:
    """Сохраняет аудио с уникальным именем"""
    timestamp = int(time.time())
    random_str = secrets.token_hex(3)
    filename = f"user_{user_id}_{timestamp}_{random_str}.mp3"

    path = Path("data/music") / filename
    path.write_bytes(file_bytes)

    return str(path)

# Часть 2: Работа с API
def get_weather(city: str) -> dict:
    """Получает погоду с OpenWeatherMap в градусах Цельсия"""
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={Config.OPENWEATHER_API_KEY}"
        f"&units=metric&lang=ru"  # Добавлены параметры
    )
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None