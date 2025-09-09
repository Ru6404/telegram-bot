#!/bin/bash
echo "📊 СТАТУС СЕРВЕРА"

# Проверяем запущен ли сервер
if pgrep -f "uvicorn main:app" > /dev/null; then
    # Пытаемся узнать порт
    PORT=$(ps aux | grep "uvicorn main:app" | grep -o "port [0-9]*" | awk '{print $2}' | head -1)
    
    if [ -z "$PORT" ]; then
        PORT=$(cat ~/.cloud-api-port 2>/dev/null || echo "unknown")
    fi
    
    echo "✅ Сервер запущен на порту: $PORT"
    echo "🌐 URL: http://localhost:$PORT"
    echo "🖥️  Веб: http://localhost:$PORT/web"
    
    # Проверяем работу
    echo "🧪 Проверяем ответ сервера..."
    timeout 5s curl -s http://localhost:$PORT/health >/dev/null && echo "✅ Сервер отвечает" || echo "❌ Сервер не отвечает"
    
else
    echo "❌ Сервер не запущен"
    echo "💡 Запусти: ./universal-start.sh"
fi
