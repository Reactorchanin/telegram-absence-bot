import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from storage import StatsStorage
from utils import (
    extract_user_from_message, 
    format_absence_message, 
    format_stats_by_levels,
    format_user_stats_message,
    is_admin,
    get_user_display_name
)

logger = logging.getLogger(__name__)
router = Router()
storage = StatsStorage()

@router.message(Command("непришел", "neprishel"))
async def handle_absence_command(message: Message):
    """Обработчик команды /непришел или /neprishel"""
    try:
        # Извлекаем информацию о пользователе
        user_info = extract_user_from_message(message)
        
        if not user_info:
            await message.reply(
                "❌ Укажите пользователя через @username или ответьте на его сообщение командой /непришел"
            )
            return
        
        user_id, username = user_info
        
        # Добавляем прогул
        count = storage.add_absence(user_id, username)
        
        # Форматируем и отправляем ответ
        response = format_absence_message(username, count)
        await message.reply(response)
        
        logger.info(f"Прогул засчитан: {username} ({user_id}) - {count}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке команды непришел: {e}")
        await message.reply("❌ Произошла ошибка при обработке команды")

@router.message(Command("стата", "stats"))
async def handle_stats_command(message: Message):
    """Обработчик команды /стата или /stats"""
    try:
        # Получаем всю статистику
        stats = storage.get_all_stats()
        
        # Форматируем и отправляем ответ
        response = format_stats_by_levels(stats)
        await message.reply(response)
        
        logger.info(f"Статистика запрошена пользователем {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке команды стата: {e}")
        await message.reply("❌ Произошла ошибка при получении статистики")

@router.message(Command("сколько"))
async def handle_user_stats_command(message: Message):
    """Обработчик команды /сколько для получения статистики конкретного пользователя"""
    try:
        # Извлекаем информацию о пользователе
        user_info = extract_user_from_message(message)
        
        if not user_info:
            await message.reply(
                "❌ Укажите пользователя через @username или ответьте на его сообщение командой /сколько"
            )
            return
        
        user_id, username = user_info
        
        # Получаем количество прогулов
        count = storage.get_absences(user_id)
        
        # Форматируем и отправляем ответ
        response = format_user_stats_message(username, count)
        await message.reply(response)
        
        logger.info(f"Статистика пользователя запрошена: {username} ({user_id}) - {count}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке команды сколько: {e}")
        await message.reply("❌ Произошла ошибка при получении статистики пользователя")

@router.message(Command("resetstats"))
async def handle_reset_stats_command(message: Message):
    """Обработчик команды /resetstats для сброса статистики (только для админов)"""
    try:
        # Проверяем права администратора
        if not is_admin(message.from_user):
            await message.reply("❌ У вас нет прав для выполнения этой команды")
            return
        
        # Сбрасываем статистику
        storage.reset_stats()
        
        await message.reply("✅ Статистика прогулов сброшена")
        
        logger.info(f"Статистика сброшена администратором {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при сбросе статистики: {e}")
        await message.reply("❌ Произошла ошибка при сбросе статистики")

@router.message(Command("help", "помощь"))
async def handle_help_command(message: Message):
    """Обработчик команды /help или /помощь"""
    help_text = """
🤖 Бот для учёта прогулов

📋 Доступные команды:

/непришел @username - Засчитать прогул пользователю
/neprishel @username - Альтернативная команда
/стата - Показать статистику всех прогульщиков
/stats - Альтернативная команда
/сколько @username - Показать статистику конкретного пользователя
/resetstats - Сбросить всю статистику (только для админов)
/help - Показать эту справку

💡 Как использовать:
• Напишите /непришел @username для засчитывания прогула
• Или ответьте на сообщение пользователя командой /непришел
• Используйте /стата для просмотра общего рейтинга
"""
    
    await message.reply(help_text) 
       
