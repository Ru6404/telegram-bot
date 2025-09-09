#!/bin/bash
echo "🛑 ОСТАНОВКА СЕРВЕРА"

# Останавливаем все uvicorn процессы
pkill -f "uvicorn main:app" 2>/dev/null

# Удаляем файл с портом
rm -f ~/.cloud-api-port 2>/dev/null

echo "✅ Все серверы остановлены"
echo "📋 Проверяем:"
ps aux | grep uvicorn | grep -v grep || echo "✅ Серверов не найдено"
