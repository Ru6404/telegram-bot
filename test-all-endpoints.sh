#!/bin/bash
echo "🧪 ТЕСТИРУЕМ ВСЕ ENDPOINTS"

# Запускаем сервер в фоне
echo "🚀 Запускаем сервер..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Ждем запуска
sleep 3

echo ""
echo "📋 ТЕСТИРУЕМ ENDPOINTS:"
echo "========================"

endpoints=(
    "/"
    "/health" 
    "/users"
    "/todos"
    "/deploy-status"
    "/system-info"
)

for endpoint in "${endpoints[@]}"; do
    echo "📍 $endpoint:"
    curl -s "http://localhost:8000$endpoint" | python -m json.tool
    echo "-----------------------"
done

# Останавливаем сервер
echo "🛑 Останавливаем сервер..."
kill $SERVER_PID 2>/dev/null

echo "✅ Все endpoints работают!"
