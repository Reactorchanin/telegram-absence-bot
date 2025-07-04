# 📦 Установка и настройка

Подробная инструкция по установке Python и настройке Telegram-бота.

## 🐍 Установка Python

### Windows

1. **Скачайте Python:**
   - Перейдите на [python.org](https://python.org)
   - Скачайте последнюю версию Python 3.11 или выше
   - Выберите "Windows installer (64-bit)"

2. **Установите Python:**
   - Запустите скачанный файл
   - **ВАЖНО:** Отметьте галочку "Add Python to PATH"
   - Выберите "Install Now"
   - Дождитесь завершения установки

3. **Проверьте установку:**
   ```cmd
   python --version
   pip --version
   ```

### macOS

1. **Используйте Homebrew (рекомендуется):**
   ```bash
   # Установка Homebrew (если не установлен)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Установка Python
   brew install python
   ```

2. **Или скачайте с python.org:**
   - Перейдите на [python.org](https://python.org)
   - Скачайте версию для macOS
   - Установите скачанный файл

3. **Проверьте установку:**
   ```bash
   python3 --version
   pip3 --version
   ```

### Linux (Ubuntu/Debian)

1. **Обновите систему:**
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Установите Python:**
   ```bash
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Проверьте установку:**
   ```bash
   python3 --version
   pip3 --version
   ```

## 🤖 Создание Telegram-бота

### 1. Получение токена

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Введите имя бота (например: "Absence Tracker")
4. Введите username бота (например: "my_absence_bot")
5. Скопируйте полученный токен

### 2. Настройка бота

1. **Создайте файл `.env`:**
   ```bash
   # В папке проекта
   echo "BOT_TOKEN=your_token_here" > .env
   ```

2. **Замените `your_token_here` на ваш токен**

### 3. Настройка прав бота

1. Добавьте бота в группу
2. Сделайте бота администратором группы
3. Включите права:
   - Отправка сообщений
   - Чтение сообщений
   - Удаление сообщений (опционально)

## 🚀 Запуск бота

### Windows

1. **Откройте командную строку в папке проекта:**
   ```cmd
   cd "путь\к\telegram_absence_bot"
   ```

2. **Установите зависимости:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Запустите бота:**
   ```cmd
   python main.py
   ```

### macOS/Linux

1. **Откройте терминал в папке проекта:**
   ```bash
   cd путь/к/telegram_absence_bot
   ```

2. **Установите зависимости:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Запустите бота:**
   ```bash
   python3 main.py
   ```

### Использование скриптов запуска

#### Windows
```cmd
start.bat
```

#### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

## 🧪 Тестирование

После установки зависимостей запустите тесты:

```bash
# Windows
python test_bot.py

# macOS/Linux
python3 test_bot.py
```

Вы должны увидеть:
```
🤖 Тестирование Telegram-бота для учёта прогулов
==================================================
🧪 Тестирование модуля хранения данных...
✅ Тесты хранения данных пройдены!
🧪 Тестирование функций форматирования...
✅ Тесты форматирования пройдены!
🎉 Все тесты пройдены успешно!
```

## 🔧 Устранение проблем

### Python не найден

**Windows:**
```cmd
# Проверьте, добавлен ли Python в PATH
echo %PATH%

# Если нет, добавьте вручную:
# C:\Users\YourName\AppData\Local\Programs\Python\Python311\
# C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts\
```

**macOS/Linux:**
```bash
# Проверьте установку
which python3
which pip3

# Если не установлен
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python                   # macOS
```

### Ошибки с pip

```bash
# Обновите pip
python -m pip install --upgrade pip

# Или
pip3 install --upgrade pip
```

### Ошибки с зависимостями

```bash
# Удалите и переустановите
pip uninstall aiogram python-dotenv
pip install -r requirements.txt
```

### Проблемы с правами доступа

**Windows:**
- Запустите командную строку от имени администратора

**macOS/Linux:**
```bash
# Используйте sudo для установки
sudo pip3 install -r requirements.txt

# Или используйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## 📱 Использование в группе

1. **Добавьте бота в группу**
2. **Сделайте бота администратором**
3. **Протестируйте команды:**
   ```
   /help - показать справку
   /непришел @username - засчитать прогул
   /стата - показать статистику
   ```

## 🔒 Безопасность

1. **Никогда не делитесь токеном бота**
2. **Не коммитьте файл .env в Git**
3. **Используйте разные токены для разработки и продакшена**
4. **Регулярно обновляйте зависимости**

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте раздел "Устранение проблем"
2. Убедитесь, что Python установлен корректно
3. Проверьте логи в файле `bot.log`
4. Создайте Issue в репозитории проекта

---

**Удачной установки! 🎉** 