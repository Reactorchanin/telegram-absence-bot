@echo off
echo 🤖 Запуск Telegram-бота для учёта прогулов...
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python с https://python.org
    pause
    exit /b 1
)

REM Проверяем наличие .env файла
if not exist ".env" (
    echo ⚠️  Файл .env не найден!
    echo Создайте файл .env с содержимым:
    echo BOT_TOKEN=your_bot_token_here
    echo.
    echo Получите токен у @BotFather в Telegram
    pause
    exit /b 1
)

REM Устанавливаем зависимости
echo 📦 Установка зависимостей...
pip install -r requirements.txt

REM Запускаем бота
echo 🚀 Запуск бота...
python main.py

pause 