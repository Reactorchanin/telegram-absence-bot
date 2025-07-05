import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import BOT_TOKEN, LOG_FILE
from handlers import router

# Настройка логирования
def setup_logging():
    """Настраивает логирование"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="непришел", description="Засчитать прогул пользователю"),
        BotCommand(command="снял", description="Снять прогул (только для админов)"),
        BotCommand(command="стата", description="Показать статистику всех прогульщиков"),
        BotCommand(command="сколько", description="Показать статистику пользователя"),
        BotCommand(command="resetstats", description="Сбросить всю статистику (только для админов)"),
        BotCommand(command="help", description="Показать справку")
    ]
    await bot.set_my_commands(commands)

async def main():
    """Основная функция запуска бота"""
    # Настраиваем логирование
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Проверяем наличие токена
    if not BOT_TOKEN:
        logger.error("❌ Не указан токен бота! Создайте файл .env с BOT_TOKEN=your_token")
        return
    
    # Создаём объекты бота и диспетчера
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Регистрируем роутеры
    dp.include_router(router)
    
    # Обработчик запуска
    @dp.startup()
    async def on_startup():
        logger.info("🚀 Бот запущен!")
        logger.info("📊 Бот для учёта прогулов готов к работе")
        await set_bot_commands(bot)
    
    # Обработчик остановки
    @dp.shutdown()
    async def on_shutdown():
        logger.info("🛑 Бот остановлен")
    
    try:
        # Запускаем бота
        logger.info("🔄 Запуск бота...")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("⏹️ Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        # Закрываем сессию бота
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}") 
        #лол