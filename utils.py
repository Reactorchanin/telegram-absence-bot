import re
import random
from typing import Optional, Tuple
from aiogram.types import Message, User

# Структура уровней и титулов
LEVELS = [
    {
        "min": 1, "max": 4,
        "emoji": "🔥", "title": "УРОВЕНЬ 1: СЛИЗНЯКИ-ОБЕЩАЛЬЩИКИ",
        "nicknames": [
            '«„Приду!“ — сказал и сдох в телефоне»',
            '«Герой пиздежа: 100% слова, 0% явки»',
            '«Обещал как царь, приперся как мусор»',
            '«Словоблуд диванного разлива»',
            '«Говно, забывшее про клятвы»',
        ]
    },
    {
        "min": 5, "max": 9,
        "emoji": "💩", "title": "УРОВЕНЬ 2: ПРЕДАТЕЛИ БУХЛИЧНОГО ФРОНТА",
        "nicknames": [
            '«Изменник водочного доверия»',
            '«Дезертир шоты-дринки»',
            '«Шаурма, сбежавшая до твоего прихода»',
            '«Загубленный тост в пустоте»',
            '«Пробка от шампанского без праздника»',
        ]
    },
    {
        "min": 10, "max": 14,
        "emoji": "☠️", "title": "УРОВЕНЬ 3: КЛОУНЫ БЕЗ ЦИРКА",
        "nicknames": [
            '«Клоун-невидимка (обещал фокус, слил воду)»',
            '«Шут гороховый с тухлыми анекдотами»',
            '«Уёбок, оставивший нас без смеха»',
            '«Скоморох сраных оправданий»',
            '«Фигура молчания на месте дурака»',
        ]
    },
    {
        "min": 15, "max": 19,
        "emoji": "🪓", "title": "УРОВЕНЬ 4: ЭПИЧЕСКИЕ ГОВНОПИСЦЫ",
        "nicknames": [
            '«Свиток пустых обещаний (сожжён)»',
            '«Поэт-пессимист: строфа „не приду“»',
            '«Баллада о трусливой мокрице»',
            '«Рифмоплёт говна и измены»',
            '«Гомер пиздеца (Илиада неявки)»',
        ]
    },
    {
        "min": 20, "max": 24,
        "emoji": "🧨", "title": "УРОВЕНЬ 5: МАНЬЯКИ НАШЕГО ТЕРПЕНИЯ",
        "nicknames": [
            '«Серийный убийца планов»',
            '«Доктор Блевотный: вскрыл надежды»',
            '«Психопат с синдромом „забил хуй“»',
            '«Маньяк-одиночка: жертва — наша тусовка»',
            '«Ганнибал без смелости (сожрал слово)»',
        ]
    },
    {
        "min": 25, "max": 29,
        "emoji": "⚡", "title": "УРОВЕНЬ 6: БОГИ ИЗВРАЩЁННОГО ПИЗДЕЖА",
        "nicknames": [
            '«Зевс-пиздабол: метнул молчание вместо молнии»',
            '«Один-одноглазый (не увидел наш чат)»',
            '«Анубис — взвесил твою душу и сблевал»',
            '«Локи лжи: слил, как истинный тролль»',
            '«Бастет-стерва: нассала на наши надежды»',
        ]
    },
    {
        "min": 30, "max": 34,
        "emoji": "🌑", "title": "УРОВЕНЬ 7: КОСМИЧЕСКИЕ МУДАКИ",
        "nicknames": [
            '«Чёрная дыра обещаний (поглотила 5 литров пива)»',
            '«Спутник вранья на орбите игнора»',
            '«Инопланетянин: „Было дело... но улетел“»',
            '«Кометный хвост твоего позора»',
            '«Туманность: там, где должно быть твое тело»',
        ]
    },
    {
        "min": 35, "max": 39,
        "emoji": "🔪", "title": "УРОВЕНЬ 8: ПАЛАЧИ НАШЕГО ВЕЧЕРА",
        "nicknames": [
            '«Экзекутор: казнил наш настрой»',
            '«Душитель смеха (руки — твои смс)»',
            '«Палач-молчун: гильотина для планов»',
            '«Садист тишины: замучил ожиданием»',
            '«Гробовщик веселья (закопал тусу)»',
        ]
    },
    {
        "min": 40, "max": 44,
        "emoji": "💎", "title": "УРОВЕНЬ 9: АБСОЛЮТНЫЕ УРОДЫ СИСТЕМЫ",
        "nicknames": [
            '«Идеальный шторм пиздеца: слил без предупреждения»',
            '«Эталонное говно в вакууме совести»',
            '«Кристалл лжи (огранка „нахуй нужен“)»',
            '«Бриллиантовая жопа: 100 карат стыда»',
            '«Алмазный член: твёрд в обещаниях, мягок в явке»',
        ]
    },
    {
        "min": 45, "max": 1000,
        "emoji": "☯️", "title": "УРОВЕНЬ 10: ДНО МАТЕРИНСКОГО ПРОКЛЯТИЯ",
        "nicknames": [
            '«Сын шлюхи безотцовщины (мать звонила — ты врал)»',
            '«Бесбашенный уёбок: за рулём отмазок»',
            '«Пизда абьюза: сломал наши ожидания»',
            '«Карма-убийца: вернётся тройным пиздецом»',
            '«Приговор: ПОЗОР НА ВЕК × фото в чате на унитазе»',
        ]
    },
]

# Определение уровня по количеству прогулов
def get_level(absences: int):
    for i, level in enumerate(LEVELS):
        if level["min"] <= absences <= level["max"]:
            return i, level
    return None, None

def extract_user_from_message(message: Message) -> Optional[Tuple[str, str]]:
    # ... (оставить без изменений)
    if message.reply_to_message and message.reply_to_message.from_user:
        user = message.reply_to_message.from_user
        return str(user.id), user.username or user.first_name or str(user.id)
    text = message.text or message.caption or ""
    username_match = re.search(r'@(\w+)', text)
    if username_match:
        username = username_match.group(1)
        return username, username
    return None

def format_stats_by_levels(stats: dict) -> str:
    """Форматирует статистику по уровням и титулам"""
    levels_users = {i: [] for i in range(len(LEVELS))}
    for user_id, absences in stats.items():
        if absences < 1:
            continue
        idx, level = get_level(absences)
        if idx is not None:
            nickname = random.choice(level["nicknames"])
            levels_users[idx].append((user_id, absences, nickname))
    result = []
    for idx, level in enumerate(LEVELS):
        users = levels_users[idx]
        if not users:
            continue
        result.append(f"{level['emoji']} {level['title']}")
        for user_id, absences, nickname in users:
            result.append(f"@{user_id} — {nickname} ({absences} прогулов)")
        result.append("")
    if not result:
        return "Пока никто не прогуливал! 🎉"
    return "\n".join(result)

def format_absence_message(username: str, absences: int) -> str:
    idx, level = get_level(absences)
    if level:
        nickname = random.choice(level["nicknames"])
        return f"@{username} — БЛЯДЬ, ТЫ ОБЕЩАЛ! ТЕПЕРЬ ТЫ {nickname} ({absences} прогулов). ПИЗДЫ ЖДИ В ЛИЧКУ + 1 ШОТ В ДОЛГ!"
    else:
        return f"@{username} теперь {absences} прогул(а/ов)"

def is_admin(user: User) -> bool:
    return True

def get_user_display_name(user: User) -> str:
    if user.username:
        return f"@{user.username}"
    elif user.first_name:
        return user.first_name
    else:
        return str(user.id)
        
def format_user_stats_message(username: str, count: int) -> str:
    idx, level = get_level(count)
    if count == 0:
        return f"@{username} пока не прогуливал! 🎉"
    elif level:
        nickname = random.choice(level["nicknames"])
        return f"@{username} — {nickname} ({count} прогулов)"
    else:
        return f"@{username} прогулял {count} раз"