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
    format_remove_absence_message,
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
                "❌ Укажи прогульщика через @username , придурок или на его сообщение ответь с командой /непришел"
            )
            return
        
        user_id, username = user_info
        
        # Добавляем прогул
        count = storage.add_absence(user_id, username)
        
        # Форматируем и отправляем ответ
        response = format_absence_message(username, count)
        await message.reply(response)
        
        logger.info(f"Проёб засчитан: {username} ({user_id}) - {count}")
        
    except Exception as e:
        logger.error(f"Какая-то хуйня при обработке команды непришел: {e}")
        await message.reply("❌ Произошла какая-то ебала при обработке команды")

@router.message(Command("снял", "snyal"))
async def handle_remove_absence_command(message: Message):
    """Обработчик команды /снял для снятия прогула (только для админов)"""
    try:
        # Проверяем права администратора
        if not is_admin(message.from_user):
            await message.reply("❌ Писька ещё не доросла это жмать")
            return
        
        # Извлекаем информацию о пользователе
        user_info = extract_user_from_message(message)
        
        if not user_info:
            await message.reply(
                "❌ Укажи святошу через @username или ответь на его пердёж командой /снял"
            )
            return
        
        user_id, username = user_info
        
        # Снимаем прогул
        success = storage.remove_absence(user_id)
        response = format_remove_absence_message(username, success)
        await message.reply(response)
            
        logger.info(f"Снят прогул: {username} ({user_id}) гигачадом {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при снятии прогула: {e}")
        await message.reply("❌ Произошла ошибка при снятии прогула")

@router.message(Command("стата", "stats"))
async def handle_stats_command(message: Message):
    """Обработчик команды /стата или /stats"""
    try:
        # Получаем всю статистику
        stats = storage.get_all_stats()
        
        # Форматируем и отправляем ответ
        response = format_stats_by_levels(stats)
        await message.reply(response)
        
        logger.info(f"Статистику узнать захотел? {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Проебал код команды стата: {e}")
        await message.reply("❌ Наебалась твоя статистика")

@router.message(Command("сколько", "skolko"))
async def handle_user_stats_command(message: Message):
    """Обработчик команды /сколько для получения статистики конкретного пользователя"""
    try:
        # Извлекаем информацию о пользователе
        user_info = extract_user_from_message(message)
        
        if not user_info:
            await message.reply(
                "❌ Укажи проёбщика через @username или ответь на его высер командой /сколько"
            )
            return
        
        user_id, username = user_info
        
        # Получаем количество прогулов
        count = storage.get_absences(user_id)
        
        # Форматируем и отправляем ответ
        response = format_user_stats_message(username, count)
        await message.reply(response)
        
        logger.info(f"Этот придурок проебался: {username} ({user_id}) - {count}")
        
    except Exception as e:
        logger.error(f"Объёб при обработке команды сколько: {e}")
        await message.reply("❌ Произошла хуйня при получении статистики кончелыги")

@router.message(Command("resetstats"))
async def handle_reset_stats_command(message: Message):
    """Обработчик команды /resetstats для сброса статистики (только для админов)"""
    try:
        # Проверяем права администратора
        if not is_admin(message.from_user):
            await message.reply("❌ Ты чо, самый умный что ли?")
            return
        
        # Сбрасываем статистику
        storage.reset_stats()
        
        await message.reply("✅ Выдохнули, ебалай на админе просрал все данные о прогулах")
        
        logger.info(f"Статистика послана нахуй администратором {message.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при просере статистики: {e}")
        await message.reply("❌ Произошла ошибка при сбросе статистического говна на вентилятор")

@router.message(Command("help", "помощь"))
async def handle_help_command(message: Message):
    """Обработчик команды /help или /помощь"""
    help_text = """
🤖 Бот для учёта прогулов

📋 Доступные команды:

/непришел @username - Засчитать прогул пользователю
/neprishel @username - Альтернативная команда
/снял @username - Снять прогул пользователю (только для админов)
/стата - Показать статистику всех прогульщиков
/stats - Альтернативная команда
/сколько @username - Показать статистику конкретного пользователя
/resetstats - Сбросить всю статистику (только для админов)
/help - Показать эту справку

💡 Как использовать:
• Напишите /непришел @username для засчитывания прогула
• Или ответьте на сообщение пользователя командой /непришел
• Используйте /снял @username для снятия прогула (только админы)
• Используйте /стата для просмотра общего рейтинга
"""
    
    await message.reply(help_text) 
       
