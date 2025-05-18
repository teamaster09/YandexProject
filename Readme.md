# 🤖 Telegram Bot Template (Python + Aiogram) (Проект Флоридовой Алины для Яндекс Лицея)

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Aiogram](https://img.shields.io/badge/aiogram-2.x-green.svg)
![Railway](https://img.shields.io/badge/hosted_on-railway.app-purple.svg)

Бот с возможностью:
- Сохранения медиафайлов
- Получения прогноза погоды
- Работы 24/7 в облаке

## 🚀 Развертывание на Railway.app

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/teamaster09/YandexProject)

### 📌 Шаги развертывания:
1. **Нажмите кнопку выше** → авторизуйтесь через GitHub
2. **Настройте переменные**:
   - `TELEGRAM_BOT_TOKEN` (получите у [@BotFather](https://t.me/BotFather))
   - `OPENWEATHER_API_KEY` (опционально, для команды `/weather`)
3. **Нажмите "Deploy"** — развертывание займет ~2 минуты

## 🛠 Локальная разработка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/teamaster09/YandexProject
cd ваш-репозиторий

# 2. Настройте окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# 3. Установите зависимости
pip install -r requirements.txt


# 4. Запустите бота
python bot.py