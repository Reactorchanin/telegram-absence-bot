#1234
import logging
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, Document
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import os

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
from config import STATS_FILE

logger = logging.getLogger(__name__)
router = Router()

# Создаем storage с логированием
logger.info("🔧 Создаем экземпляр StatsStorage...")
storage = StatsStorage()
logger.info("✅ StatsStorage создан успешно")

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
        if not message.from_user:
            await message.reply("❌ Не удалось определить пользователя.")
            return
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
            
        logger.info(f"Снят прогул: {username} ({user_id}) гигачадом {message.from_user.id if message.from_user else 'unknown'}")
        
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
        
        logger.info(f"Статистику узнать захотел? {message.from_user.id if message.from_user else 'unknown'}")
        
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
        if not message.from_user:
            await message.reply("❌ Не удалось определить пользователя.")
            return
        if not is_admin(message.from_user):
            await message.reply("❌ Ты чо, самый умный что ли?")
            return
        
        # Сбрасываем статистику
        storage.reset_stats()
        
        await message.reply("✅ Выдохнули, ебалай на админе просрал все данные о прогулах")
        
        logger.info(f"Статистика послана нахуй администратором {message.from_user.id if message.from_user else 'unknown'}")
        
    except Exception as e:
        logger.error(f"Ошибка при просере статистики: {e}")
        await message.reply("❌ Произошла ошибка при сбросе статистического говна на вентилятор")

@router.message(Command("backup"))
async def handle_backup_command(message: Message):
    """Отправляет файл статистики админу"""
    try:
        if not message.from_user:
            await message.reply("❌ Не удалось определить пользователя.")
            return
        if not is_admin(message.from_user):
            await message.reply("❌ Только админ может делать бэкап!")
            return
        if not os.path.exists(STATS_FILE):
            await message.reply("Файл статистики не найден.")
            return
        if not message.bot:
            await message.reply("❌ Не удалось получить объект бота.")
            return
        await message.reply_document(FSInputFile(STATS_FILE), caption="Вот ваш бэкап статистики!")
        logger.info(f"Бэкап статистики отправлен: {STATS_FILE}")
    except Exception as e:
        logger.error(f"Ошибка при отправке бэкапа: {e}")
        await message.reply("❌ Не удалось отправить бэкап.")

@router.message(Command("restore"))
async def handle_restore_command(message: Message, state: FSMContext):
    """Восстанавливает статистику из файла (только для админов, в ответ на файл)"""
    try:
        if not message.from_user:
            await message.reply("❌ Не удалось определить пользователя.")
            return
        if not is_admin(message.from_user):
            await message.reply("❌ Только админ может восстанавливать статистику!")
            return
        if not message.reply_to_message or not message.reply_to_message.document:
            await message.reply("Пожалуйста, ответьте командой /restore на сообщение с файлом статистики (JSON).")
            return
        document = message.reply_to_message.document
        if not message.bot:
            await message.reply("❌ Не удалось получить объект бота.")
            return
        file = await message.bot.get_file(document.file_id)
        file_path = STATS_FILE
        if not file.file_path:
            await message.reply("❌ Не удалось получить путь к файлу.")
            return
        # Сохраняем файл
        await message.bot.download_file(file.file_path, file_path)
        # Перезагружаем данные в storage
        storage.stats = storage._load_stats()
        await message.reply("✅ Статистика успешно восстановлена из файла!")
        logger.info(f"Статистика восстановлена из файла: {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при восстановлении статистики: {e}")
        await message.reply("❌ Не удалось восстановить статистику из файла.")

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
/backup - Создать бэкап статистики (только для админов)
/restore - Восстановить статистику из файла (только для админов)
/help - Показать эту справку

💡 Как использовать:
• Напишите /непришел @username для засчитывания прогула
• Или ответьте на сообщение пользователя командой /непришел
• Используйте /снял @username для снятия прогула (только админы)
• Используйте /стата для просмотра общего рейтинга
"""
    
    await message.reply(help_text) 
       
