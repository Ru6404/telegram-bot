#!/bin/bash

# Папка проекта
cd ~/cloud-api

# Проверка и установка зависимостей
pip install -r requirements.txt

# Определяем локальный IP Wi-Fi
IP=$(ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1)

echo "🌐 Локальная ссылка: http://$IP:8080"

# Запуск сервера в tmux
tmux has-session -t cloud 2>/dev/null || \
tmux new -d -s cloud "cd ~/cloud-api && uvicorn main:app --reload --host 0.0.0.0 --port 8080"

# Запуск Telegram бота в tmux
tmux has-session -t bot 2>/dev/null || \
tmux new -d -s bot "cd ~/cloud-api && export TELEGRAM_TOKEN='ВАШ_ТОКЕН_БОТА' && python bot.py"

echo "🚀 Сервер и бот запущены в фоне"
