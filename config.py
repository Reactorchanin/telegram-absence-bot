import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота (получить у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Файл для хранения статистики
import os
data_dir = os.getenv('RAILWAY_PERSISTENT_STORAGE_PATH', '.')
STATS_FILE = os.path.join(data_dir, 'stats.json')

# Логирование
LOG_FILE = 'bot.log' 