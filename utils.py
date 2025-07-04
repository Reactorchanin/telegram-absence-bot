import re
import random
from typing import Optional, Tuple
from aiogram.types import Message, User

def get_insult_title(count: int) -> str:
    """Возвращает 'обидное' название в зависимости от количества прогулов"""
    if count == 0:
        return "честный работник"
    elif count == 1:
        return random.choice([
            "прогульщик-новичок",
            "ленивец",
            "сачок"
        ])
    elif count == 2:
        return random.choice([
            "заядлый прогульщик",
            "мастер отлынивания",
            "профессиональный сачок"
        ])
    elif count == 3:
        return random.choice([
            "прогульщик-эксперт",
            "чемпион по прогулам",
            "мастер пропуска встреч"
        ])
    elif count == 4:
        return random.choice([
            "прогульщик-легенда",
            "король прогулов",
            "император сачков"
        ])
    elif count == 5:
        return random.choice([
            "прогульщик-бог",
            "непобедимый сачок",
            "мастер вселенского отлынивания"
        ])
    else:
        return random.choice([
            "прогульщик-божество",
            "абсолютный чемпион прогулов",
            "непревзойдённый мастер сачков",
            "легендарный отлыниватель",
            "король всех прогульщиков"
        ])

def extract_user_from_message(message: Message) -> Optional[Tuple[str, str]]:
    """
    Извлекает информацию о пользователе из сообщения
    Возвращает кортеж (user_id, username) или None
    """
    # Проверяем reply на сообщение
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
        return str(user.id), user.username or user.first_name or str(user.id)
    
    # Проверяем текст сообщения на наличие username
    text = message.text or message.caption or ""
    
    # Ищем @username в тексте
    username_match = re.search(r'@(\w+)', text)
    if username_match:
        username = username_match.group(1)
        # Здесь можно было бы искать user_id по username в базе,
        # но пока возвращаем username как идентификатор
        return username, username
    
    return None

def format_absence_message(username: str, count: int) -> str:
    """Форматирует сообщение о прогуле"""
    if count == 1:
        return f"@{username} теперь 1 прогул"
    elif 2 <= count <= 4:
        return f"@{username} теперь {count} прогула"
    else:
        return f"@{username} теперь {count} прогулов"

def format_stats_message(stats: dict) -> str:
    """Форматирует сообщение со статистикой"""
    if not stats:
        return "Пока никто не прогуливал! 🎉"
    
    # Сортируем по количеству прогулов (по убыванию)
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    message = "📊 Топ прогульщиков:\n\n"
    
    for user_id, count in sorted_stats:
        # Пытаемся получить username, если это возможно
        username = user_id  # По умолчанию используем user_id
        insult_title = get_insult_title(count)
        message += f"@{username} ({insult_title}): {count} прогулов\n"
    
    return message

def format_user_stats_message(username: str, count: int) -> str:
    """Форматирует сообщение о статистике конкретного пользователя"""
    if count == 0:
        return f"@{username} пока не прогуливал! 🎉"
    else:
        insult_title = get_insult_title(count)
        if count == 1:
            return f"@{username} ({insult_title}) прогулял 1 раз"
        elif 2 <= count <= 4:
            return f"@{username} ({insult_title}) прогулял {count} раза"
        else:
            return f"@{username} ({insult_title}) прогулял {count} раз"

def is_admin(user: User) -> bool:
    """Проверяет, является ли пользователь администратором"""
    # Здесь можно добавить логику проверки администратора
    # Пока возвращаем True для всех (можно настроить по user_id)
    return True

def get_user_display_name(user: User) -> str:
    """Получает отображаемое имя пользователя"""
    if user.username:
        return f"@{user.username}"
    elif user.first_name:
        return user.first_name
    else:
        return str(user.id) 