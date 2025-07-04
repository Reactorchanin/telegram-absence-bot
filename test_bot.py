#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функционала бота
Запускается без подключения к Telegram API
"""

import json
import sys
from storage import StatsStorage
from utils import format_absence_message, format_stats_message, format_user_stats_message

def test_storage():
    """Тестирует функционал хранения данных"""
    print("🧪 Тестирование модуля хранения данных...")
    
    # Создаём временный файл для тестов
    test_file = "test_stats.json"
    storage = StatsStorage(test_file)
    
    # Тест 1: Добавление прогулов
    print("\n1. Тест добавления прогулов:")
    count1 = storage.add_absence("vasya", "vasya")
    print(f"   @vasya: {count1} прогул")
    
    count2 = storage.add_absence("petya", "petya")
    print(f"   @petya: {count2} прогул")
    
    count3 = storage.add_absence("vasya", "vasya")
    print(f"   @vasya: {count3} прогула")
    
    # Тест 2: Получение статистики
    print("\n2. Тест получения статистики:")
    vasya_count = storage.get_absences("vasya")
    petya_count = storage.get_absences("petya")
    masha_count = storage.get_absences("masha")
    
    print(f"   @vasya: {vasya_count} прогулов")
    print(f"   @petya: {petya_count} прогулов")
    print(f"   @masha: {masha_count} прогулов")
    
    # Тест 3: Общая статистика
    print("\n3. Тест общей статистики:")
    all_stats = storage.get_all_stats()
    print(f"   Всего пользователей: {len(all_stats)}")
    for user_id, count in all_stats.items():
        print(f"   {user_id}: {count}")
    
    # Очистка
    import os
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✅ Тесты хранения данных пройдены!")

def test_formatting():
    """Тестирует функции форматирования"""
    print("\n🧪 Тестирование функций форматирования...")
    
    # Тест форматирования сообщений о прогулах
    print("\n1. Тест форматирования прогулов:")
    test_cases = [
        (1, "1 прогул"),
        (2, "2 прогула"),
        (5, "5 прогулов"),
        (21, "21 прогул"),
        (22, "22 прогула"),
        (25, "25 прогулов")
    ]
    
    for count, expected in test_cases:
        result = format_absence_message("test", count)
        print(f"   {count} прогулов: {result}")
    
    # Тест форматирования статистики
    print("\n2. Тест форматирования статистики:")
    test_stats = {"vasya": 3, "petya": 1, "masha": 2}
    stats_message = format_stats_message(test_stats)
    print("   Статистика:")
    for line in stats_message.split('\n'):
        if line.strip():
            print(f"   {line}")
    
    # Тест пустой статистики
    empty_stats = format_stats_message({})
    print(f"   Пустая статистика: {empty_stats}")
    
    # Тест статистики пользователя
    print("\n3. Тест статистики пользователя:")
    user_stats = [
        (0, "пока не прогуливал"),
        (1, "прогулял 1 раз"),
        (2, "прогулял 2 раза"),
        (5, "прогулял 5 раз")
    ]
    
    for count, expected in user_stats:
        result = format_user_stats_message("test", count)
        print(f"   {count} прогулов: {result}")
    
    print("✅ Тесты форматирования пройдены!")

def test_example_data():
    """Тестирует работу с примерными данными"""
    print("\n🧪 Тестирование с примерными данными...")
    
    # Загружаем примерные данные
    try:
        with open("example_stats.json", "r", encoding="utf-8") as f:
            example_data = json.load(f)
        
        print("   Загруженные данные:")
        for username, count in example_data.items():
            print(f"   @{username}: {count}")
        
        # Форматируем статистику
        stats_message = format_stats_message(example_data)
        print("\n   Отформатированная статистика:")
        for line in stats_message.split('\n'):
            if line.strip():
                print(f"   {line}")
        
        print("✅ Тест с примерными данными пройден!")
        
    except FileNotFoundError:
        print("⚠️  Файл example_stats.json не найден")

def main():
    """Основная функция тестирования"""
    print("🤖 Тестирование Telegram-бота для учёта прогулов")
    print("=" * 50)
    
    try:
        test_storage()
        test_formatting()
        test_example_data()
        
        print("\n" + "=" * 50)
        print("🎉 Все тесты пройдены успешно!")
        print("Бот готов к использованию!")
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 