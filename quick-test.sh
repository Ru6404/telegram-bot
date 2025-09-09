#!/bin/bash
echo "⚡ БЫСТРАЯ ПРОВЕРКА РАБОТОСПОСОБНОСТИ"

# Проверяем зависимости
echo "📦 Проверяем зависимости..."
python -c "
from main import app, users_db, todos_db
print('✅ FastAPI приложение импортируется')
print(f'✅ Пользователей: {len(users_db)}')
print(f'✅ Задач: {len(todos_db)}')
print('✅ Все модули работают')
"

# Проверяем можем ли запустить
echo ""
echo "🚀 Тестовый запуск..."
timeout 5s python -m uvicorn main:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
sleep 2
curl -s http://localhost:8000/health >/dev/null && echo "✅ Сервер запускается и отвечает" || echo "❌ Ошибка запуска"
pkill -f "uvicorn main:app"
