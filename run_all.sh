#!/bin/bash
echo "🚀 Запуск сервера..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

sleep 2

echo "🤖 Запуск бота..."
python3 bot.py
