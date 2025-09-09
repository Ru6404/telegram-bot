#!/bin/bash
echo "⚡ БЫСТРЫЙ ТЕСТ СЕРВЕРА"

# Находим свободный порт
PORT=$(python -c "import socket; s=socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()")

echo "🔧 Запускаем тестовый сервер на порту $PORT..."
timeout 10s python -m uvicorn main:app --host 0.0.0.0 --port $PORT > /dev/null 2>&1 &

sleep 3

echo "🧪 Тестируем endpoints:"
curl -s http://localhost:$PORT/ | python -m json.tool && echo "✅ Главная страница"
curl -s http://localhost:$PORT/health | python -m json.tool && echo "✅ Health check"
curl -s http://localhost:$PORT/users | python -m json.tool && echo "✅ Пользователи"

pkill -f "uvicorn main:app" 2>/dev/null
echo "🎯 Тест завершен!"
