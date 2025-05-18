from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from app.models import User, UserFile  # Импорт моделей
from app.database import SessionLocal  # Импорт сессии БД
from app.services import save_image, save_audio
from aiogram.dispatcher import FSMContext
from app.services import get_weather
from datetime import datetime
from aiogram.dispatcher.filters.state import StatesGroup, State
import os


class WeatherStates(StatesGroup):
    waiting_for_city = State()

def register_handlers(dp):
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        with SessionLocal() as session:
            # Проверяем существование пользователя
            user = session.query(User).filter_by(telegram_id=message.from_user.id).first()

            if not user:
                # Создаем нового пользователя
                new_user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name
                )
                session.add(new_user)
                session.commit()

                # Создаем инлайн-кнопку
            weather_button = InlineKeyboardButton(
                text="Узнать погоду 🌤",
                callback_data="weather_request"
            )
            keyboard = InlineKeyboardMarkup().add(weather_button)

            # Текст сообщения с кнопкой
            start_text = (
                "Привет! Я бот для сохранения файлов.\n\n"
                "📌 Отправь мне фото или аудио, и я сохраню их!\n"
                "🌤 Или узнай текущую погоду:"
            )

            await message.answer(start_text, reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data == 'weather_request')
    async def process_weather_button(callback_query: types.CallbackQuery):
        await callback_query.message.bot.answer_callback_query(callback_query.id)
        await callback_query.message.answer("Введите название города:")
        await WeatherStates.waiting_for_city.set()

    @dp.message_handler(content_types=types.ContentType.PHOTO)
    async def handle_photo(message: types.Message):
        try:
            # Создаем папку data/images если ее нет
            os.makedirs('data/images', exist_ok=True)

            # Получаем фото с наивысшим качеством
            photo = message.photo[-1]
            file_info = await message.bot.get_file(photo.file_id)
            downloaded_file = await message.bot.download_file(file_info.file_path)

            # Сохраняем изображение
            file_path = save_image(downloaded_file.read(), message.from_user.id)

            # Записываем в БД
            with SessionLocal() as session:
                file_record = UserFile(
                    user_id=message.from_user.id,
                    file_type='image',
                    file_path=file_path,
                    uploaded_at=datetime.now()
                )
                session.add(file_record)
                session.commit()

            await message.answer("Фото успешно сохранено! 🖼️")
        except Exception as e:
            await message.answer(f"Ошибка при сохранении фото: {str(e)}")
            raise e

    @dp.message_handler(content_types=types.ContentType.AUDIO)
    async def handle_audio(message: types.Message):
        try:
            # Создаем папку data/music если ее нет
            os.makedirs('data/music', exist_ok=True)

            audio = message.audio
            file_info = await message.bot.get_file(audio.file_id)
            downloaded_file = await message.bot.download_file(file_info.file_path)

            # Сохраняем аудио
            file_path = save_audio(downloaded_file.read(), message.from_user.id)

            # Записываем в БД
            with SessionLocal() as session:
                file_record = UserFile(
                    user_id=message.from_user.id,
                    file_type='music',
                    file_path=file_path,
                    uploaded_at=datetime.now()
                )
                session.add(file_record)
                session.commit()

            await message.answer("Аудиофайл успешно сохранен! 🎵")
        except Exception as e:
            await message.answer(f"Ошибка при сохранении аудио: {str(e)}")
            raise e

    @dp.message_handler(content_types=types.ContentType.DOCUMENT)
    async def handle_document(message: types.Message):
        # Дополнительная обработка файлов, отправленных как документ
        if message.document.mime_type.startswith('image/'):
            await handle_photo(message)
        elif message.document.mime_type.startswith('audio/'):
            await handle_audio(message)

    @dp.message_handler(commands=['weather'])
    async def cmd_weather(message: types.Message):
        """Обработчик команды /weather"""
        await message.answer("Введите название города:")
        await WeatherStates.waiting_for_city.set()

    @dp.message_handler(state=WeatherStates.waiting_for_city)
    async def process_city(message: types.Message, state: FSMContext):
        try:
            city = message.text
            weather = get_weather(city)

            if not weather:
                await message.answer("Не удалось получить данные о погоде")
                return

            temp = weather['main']['temp']
            feels_like = weather['main']['feels_like']
            humidity = weather['main']['humidity']
            description = weather['weather'][0]['description'].capitalize()

            reply = (
                f"🌤 Погода в {city}:\n"
                f"🌡 Температура: {temp:.1f}°C\n"
                f"💭 Ощущается как: {feels_like:.1f}°C\n"
                f"💧 Влажность: {humidity}%\n"
                f"☁ Состояние: {description}"
            )

            await message.answer(reply)
        except Exception as e:
            await message.answer(f"Ошибка при получении погоды: {str(e)}")
        finally:
            await state.finish()