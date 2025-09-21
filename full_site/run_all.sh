#!/bin/bash

# Переменные окружения
export TELEGRAM_TOKEN="твой_токен_бота"
export SITE_URL="http://0.0.0.0:8000"

# Запуск сайта в фоне
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Ждём 2 секунды
sleep 2

# Запуск бота
python3 bot_integrated.py
