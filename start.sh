#!/bin/bash

echo "🤖 Запуск Telegram-бота для учёта прогулов..."
echo

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден! Установите Python с https://python.org"
    exit 1
fi

# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден!"
    echo "Создайте файл .env с содержимым:"
    echo "BOT_TOKEN=your_bot_token_here"
    echo
    echo "Получите токен у @BotFather в Telegram"
    exit 1
fi

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Запускаем бота
echo "🚀 Запуск бота..."
python3 main.py 