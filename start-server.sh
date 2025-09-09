#!/bin/bash
cd ~/cloud-api

# Проверяем зависимости
if ! python -c "import uvicorn" 2>/dev/null; then
    echo "📦 Устанавливаем зависимости..."
    pip install fastapi uvicorn
fi

# Запускаем сервер
echo "🚀 Запускаем Auto-Cloud API..."
python -m uvicorn main:app --reload
#!/bin/bash
echo "🚀 ЗАПУСК СЕРВЕРА"

# Останавливаем старые процессы
echo "🛑 Останавливаем старые серверы..."
pkill -f "uvicorn main:app" 2>/dev/null
sleep 2

# Запускаем на свободном порту
PORT=8080
echo "🌐 Запускаем сервер на порту $PORT..."
echo "📋 Открой в браузере:"
echo "   - http://localhost:$PORT"
echo "   - http://127.0.0.1:$PORT"
echo ""
echo "🖥️  Или используй IP:"
ip=$(ip addr show 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | head -1 | awk '{print $2}' | cut -d'/' -f1)
if [ -n "$ip" ]; then
    echo "   - http://$ip:$PORT"
else
    echo "   - IP адрес не найден"
fi
echo ""
echo "⏹️  Для остановки: Ctrl+C"
echo ""

# Запускаем сервер
python -m uvicorn main:app --reload --host 0.0.0.0 --port $PORT
