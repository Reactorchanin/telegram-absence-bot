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
            '«„Приду!“ — сказал и сдох обосравшись»',
            '«Герой пиздежа: 100% слов, 0% явки»',
            '«Обещал как царь, сделал как мусор»',
            '«Словоблуд диванного разлива»',
            '«Говно, забывшее про клятвы»',
        ]
    },
    {
        "min": 5, "max": 9,
        "emoji": "💩", "title": "УРОВЕНЬ 2: ПРЕДАТЕЛИ БУХЛИЧНОГО ФРОНТА",
        "nicknames": [
            '«Изменник водочного доверия»',
            '«Дезертир шот-войск»',
            '«Шаурма в маскхалате из говна»',
            '«Загубленный тост в пустоте»',
            '«Пробка из жопы трезвенника»',
        ]
    },
    {
        "min": 10, "max": 14,
        "emoji": "☠️", "title": "УРОВЕНЬ 3: КЛОУНЫ БЕЗ ЦИРКА",
        "nicknames": [
            '«Клоун-невидимка (обещал фокус, но обосрался)»',
            '«Шут гороховый с протухшими анекдотами»',
            '«Уёбок, оставивший нас без смеха»',
            '«Скоморох сраных оправданий»',
            '«Там где ты сидел теперь наблёвано»',
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
            '«Душитель смеха (руки — твои сообщения)»',
            '«Палач-молчун: гильотина для планов»',
            '«Садист тишины: замучил ожиданием»',
            '«Гробовщик веселья (закопал тусу)»',
        ]
    },
    {
        "min": 40, "max": 44,
        "emoji": "💎", "title": "УРОВЕНЬ 9: АБСОЛЮТНЫЕ УРОДЫ СИСТЕМЫ",
        "nicknames": [
            '«Идеальный шторм пиздеца: сливал так, что разъебало полмира»',
            '«Эталонное говно в вакууме совести»',
            '«Кристалл лжи (огранка „нахуй нужен“)»',
            '«Бриллиантовая жопа: 100 карат бесстыдства»',
            '«Алмазный член: твёрд в обещаниях, висит когда надо»',
        ]
    },
    {
        "min": 45, "max": 1000,
        "emoji": "☯️", "title": "УРОВЕНЬ 10: ДНО МАТЕРИНСКОГО ПРОКЛЯТИЯ",
        "nicknames": [
            '«Сын шлюхи безотцовщины (теперь я твой батя)»',
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
        return "Пока никто не проебал тусич! 🎉"
    return "\n".join(result)

#def format_absence_message(username: str, absences: int) -> str:
#    idx, level = get_level(absences)
#    if level:
#        nickname = random.choice(level["nicknames"])
#        return f"@{username} — БЛЯДЬ, ТЫ ОБЕЩАЛ! ТЕПЕРЬ ТЫ {nickname} ({absences} прогулов). ПИЗДЫ ЖДИ В ЛИЧКУ + 1 ШОТ В ДОЛГ!"
#    else:
#        return f"@{username} теперь {absences} прогул(а/ов)"

def format_absence_message(username: str, absences: int) -> str:
    idx, level = get_level(absences)
    if level:
        phrase = random.choice(EPIC_ABSENCE_PHRASES)
        return phrase.replace("@username", f"@{username}")
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
        return f"@{username} хороший друг/другиня, остальные кайтесь суканах! 🎉"
    elif level:
        nickname = random.choice(level["nicknames"])
        return f"@{username} — {nickname} ({count} прогулов)"
    else:
        return f"@{username} проебался {count} раз"

EPIC_ABSENCE_PHRASES = [
    "@username — ЭПИЧЕСКАЯ МОКРИЦА!\nОбещал явиться — сдох в смс.\nТвоё место занял стул с бутылкой водки. Он надёжнее.",
    "ВНИМАНИЕ: @username — ПРЕДАТЕЛЬ АЛКОБРАТСТВА!\nСлил тусу как тёплый сортир в подворотне.\nНаливаем тебе штрафной шот... в воображении, уёбок!",
    "@username? НЕТ, ЭТО ЗВУК СРАВНЕВШЕЙ ТУШИ!\nТы обосрал доверие, как бомж обосрал подвал.\nТвой статус: «Психическое дерьмо на ножках».",
    "ЧУДО: @username ИСЧЕЗ ИЗ РЕАЛЬНОСТИ!\nНо вонь лжи осталась.\nЯвка: 0%. Совесть: -100%. Уважение: сожжено.",
    "@username — ГОВНЯНЫЙ ФЕНОМЕН!\nПообещал как Че Гевара — слился как шаурма в тухлом соусе.\nТеперь ты персона нон-грата (и нон-алкоголика).",
    "НАУЧНОЕ ОТКРЫТИЕ:\n@username создал чёрную дыру там, где должен был быть человек!\nЗаконы физики: сохранены. Законы братства: растоптаны.",
    "@username — ШЕДЕВР ТРУСОСТИ!\nТвоя неявка кричит: «Я — овощ с гнилой сердцевиной!»\nПрими наш плевок в твою цифровую могилу!",
    "ПРИГОВОР: @username — ВЫСЕКУТ МЕМАМИ!\nТвоя ложь — топливо для тысячи унизительных стикеров.\nГотовь жопу: первый гиф с плачущим клоуном уже летит!",
    "@username, МЫ ЗА ТОБОЙ НЕ ЗАСКУЧАЕМ!\nТвоё пустое место украсили две бутылки текилы и пакет чипсов.\nОни не предадут. А ты — говно в бокале вина.",
    "ОБЪЯВЛЕНИЕ:\nТруп @username выброшен на помойку истории!\nПричина смерти: СПГС (Синдром Подзалупной Гнилой Совести).\nПохороны: в чате, под смех и звон бокалов."
    "@{username} — БЛЯДЬ, ТЫ ОБЕЩАЛ! ТЕПЕРЬ ТЫ {nickname} ({absences} прогулов). ПИЗДЫ ЖДИ В ЛИЧКУ + 1 ШОТ В ДОЛГ!"
]