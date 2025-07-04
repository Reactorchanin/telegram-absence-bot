# 🚀 Развертывание Telegram-бота

Инструкции по развертыванию бота на различных платформах.

## 📱 Локальный запуск

### Windows
1. Установите Python с [python.org](https://python.org)
2. Скачайте проект
3. Запустите `start.bat` или выполните команды:
```cmd
pip install -r requirements.txt
python main.py
```

### Linux/Mac
1. Установите Python3
2. Скачайте проект
3. Сделайте скрипт исполняемым и запустите:
```bash
chmod +x start.sh
./start.sh
```

## ☁️ Развертывание на сервере

### VPS (Ubuntu/Debian)

1. **Подключение к серверу:**
```bash
ssh user@your-server.com
```

2. **Установка зависимостей:**
```bash
sudo apt update
sudo apt install python3 python3-pip git screen
```

3. **Клонирование проекта:**
```bash
git clone https://github.com/your-username/telegram-absence-bot.git
cd telegram-absence-bot
```

4. **Настройка бота:**
```bash
cp .env.example .env
nano .env  # Редактируем токен
```

5. **Установка зависимостей:**
```bash
pip3 install -r requirements.txt
```

6. **Запуск в screen:**
```bash
screen -S telegram-bot
python3 main.py
# Ctrl+A, затем D для отключения
```

7. **Управление процессом:**
```bash
screen -r telegram-bot  # Подключиться к сессии
screen -ls              # Список сессий
screen -X -S telegram-bot quit  # Остановить бота
```

### Docker

1. **Создайте Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

2. **Создайте docker-compose.yml:**
```yaml
version: '3.8'
services:
  telegram-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
    volumes:
      - ./stats.json:/app/stats.json
      - ./bot.log:/app/bot.log
    restart: unless-stopped
```

3. **Запуск:**
```bash
docker-compose up -d
```

### Heroku

1. **Создайте Procfile:**
```
worker: python main.py
```

2. **Создайте runtime.txt:**
```
python-3.11.0
```

3. **Развертывание:**
```bash
heroku create your-bot-name
heroku config:set BOT_TOKEN=your_token_here
git push heroku main
heroku ps:scale worker=1
```

### Railway

1. Подключите GitHub репозиторий
2. Добавьте переменную окружения `BOT_TOKEN`
3. Railway автоматически развернет бота

## 🔧 Настройка автозапуска

### systemd (Linux)

1. **Создайте сервис:**
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

2. **Содержимое файла:**
```ini
[Unit]
Description=Telegram Absence Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/telegram-absence-bot
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Активация:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

### Supervisor

1. **Установка:**
```bash
sudo apt install supervisor
```

2. **Конфигурация:**
```bash
sudo nano /etc/supervisor/conf.d/telegram-bot.conf
```

3. **Содержимое:**
```ini
[program:telegram-bot]
command=python3 /path/to/telegram-absence-bot/main.py
directory=/path/to/telegram-absence-bot
user=your-username
autostart=true
autorestart=true
stderr_logfile=/var/log/telegram-bot.err.log
stdout_logfile=/var/log/telegram-bot.out.log
```

4. **Перезапуск:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start telegram-bot
```

## 📊 Мониторинг

### Логи
```bash
# Просмотр логов
tail -f bot.log

# Поиск ошибок
grep "ERROR" bot.log

# Статистика использования
grep "Прогул засчитан" bot.log | wc -l
```

### Статус бота
```bash
# Проверка процесса
ps aux | grep python

# Проверка файлов
ls -la stats.json bot.log
```

## 🔒 Безопасность

### Переменные окружения
- Никогда не коммитьте `.env` файл
- Используйте разные токены для разработки и продакшена
- Регулярно обновляйте токены

### Права доступа
```bash
# Ограничение прав на файлы
chmod 600 .env
chmod 644 stats.json
chmod 644 bot.log
```

### Firewall
```bash
# Ограничение доступа к серверу
sudo ufw allow ssh
sudo ufw enable
```

## 🔄 Обновления

### Автоматические обновления
```bash
#!/bin/bash
cd /path/to/telegram-absence-bot
git pull
pip3 install -r requirements.txt
sudo systemctl restart telegram-bot
```

### Резервное копирование
```bash
# Создание бэкапа
cp stats.json stats.json.backup.$(date +%Y%m%d)

# Восстановление
cp stats.json.backup.20231201 stats.json
```

## 🆘 Устранение проблем

### Бот не отвечает
1. Проверьте логи: `tail -f bot.log`
2. Проверьте статус: `systemctl status telegram-bot`
3. Проверьте токен: `echo $BOT_TOKEN`

### Ошибки с данными
1. Проверьте права: `ls -la stats.json`
2. Проверьте диск: `df -h`
3. Восстановите из бэкапа

### Высокая нагрузка
1. Мониторинг ресурсов: `htop`
2. Ограничение логов
3. Оптимизация кода

---

**Удачного развертывания! 🚀** 