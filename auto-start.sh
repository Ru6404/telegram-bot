#!/bin/bash
echo "🚀 Запуск Auto-Cloud API..."
cd ~/cloud-api

# Проверяем, не запущен ли уже сервер
if ! pgrep -f "uvicorn main:app" > /dev/null; then
    echo "✅ Сервер не запущен, запускаем..."
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
    echo "⏳ Ожидаем запуск сервера..."
    sleep 3
    
    # Проверяем статус
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "🎉 Сервер успешно запущен!"
        echo "🌐 Адрес: http://localhost:8000"
        echo "📊 Статус: $(curl -s http://localhost:8000/health | python -c 'import json,sys;print(json.load(sys.stdin)["status"])')"
    else
        echo "❌ Ошибка запуска сервера"
    fi
else
    echo "✅ Сервер уже запущен"
    echo "🌐 Адрес: http://localhost:8000"
fi

echo "📋 Доступные команды:"
echo "  curl http://localhost:8000/          - Главная страница"
echo "  curl http://localhost:8000/users     - Список пользователей"
echo "  curl http://localhost:8000/todos     - Список задач"
echo "  curl http://localhost:8000/health    - Статус здоровья"
