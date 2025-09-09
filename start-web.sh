#!/bin/bash
echo "🌐 ЗАПУСК ВЕБ-СЕРВЕРА ДЛЯ БРАУЗЕРА"

# Останавливаем старые процессы
pkill -f "uvicorn main:app" 2>/dev/null

# Запускаем сервер
echo "🚀 Запускаем сервер на порту 8000..."
echo "📋 Открой в браузере:"
echo "   - http://localhost:8000"
echo "   - http://127.0.0.1:8000" 
echo ""
echo "🖥️  Или используй IP:"
ip=$(ip addr show | grep "inet " | grep -v "127.0.0.1" | head -1 | awk '{print $2}' | cut -d'/' -f1)
echo "   - http://$ip:8000"
echo ""
echo "⏹️  Для остановки: Ctrl+C"
echo ""

# Запускаем сервер
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
