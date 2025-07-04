import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Файл для хранения статистики
STATS_FILE = 'stats.json'

# Логирование
LOG_FILE = 'bot.log' 