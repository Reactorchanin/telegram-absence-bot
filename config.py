import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Файл для хранения статистики
data_dir = os.getenv('RAILWAY_PERSISTENT_STORAGE_PATH', '.')
STATS_FILE = os.path.join(data_dir, 'stats.json')

# Логируем настройки для отладки
print(f"🔧 Настройки storage:")
print(f"   RAILWAY_PERSISTENT_STORAGE_PATH: {os.getenv('RAILWAY_PERSISTENT_STORAGE_PATH', 'НЕ УСТАНОВЛЕНА')}")
print(f"   data_dir: {data_dir}")
print(f"   STATS_FILE: {STATS_FILE}")

# Логирование
LOG_FILE = 'bot.log'

#говнирование