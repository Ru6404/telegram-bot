#!/bin/bash
echo "🔧 ЗАПУСК СЕРВЕРА В ФОНЕ"

# Останавливаем старые процессы
pkill -f "uvicorn main:app" 2>/dev/null

# Ищем свободный порт
PORT=$(python -c "import socket; s=socket.socket(); s.bind(('', 0)); print(s.getsockname()[1]); s.close()")

echo "🌐 Запускаем сервер на порту $PORT в фоне..."
nohup python -m uvicorn main:app --host 0.0.0.0 --port $PORT > server.log 2>&1 &

sleep 3

echo "✅ Сервер запущен на порту $PORT"
echo "📋 Логи: tail -f server.log"
echo "🌐 URL: http://localhost:$PORT"
echo "🖥️  Веб-интерфейс: http://localhost:$PORT/web"

# Сохраняем порт в файл
echo $PORT > ~/.cloud-api-port
echo "🎯 Порт сохранен: ~/.cloud-api-port"
