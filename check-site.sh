#!/bin/bash
echo "🌐 ПРОВЕРКА ФУНКЦИОНИРОВАНИЯ САЙТА"

echo "1. 🚀 Запускаем сервер..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

echo "2. ⏳ Ждем запуска..."
sleep 3

echo "3. 🔍 Проверяем endpoints:"
echo "   📍 Главная страница:"
curl -s http://localhost:8000/ | python -m json.tool

echo ""
echo "   ❤️ Health check:"
curl -s http://localhost:8000/health | python -m json.tool

echo ""
echo "   👥 Пользователи:"
curl -s http://localhost:8000/users | python -m json.tool

echo ""
echo "   ✅ Tasks:"
curl -s http://localhost:8000/todos | python -m json.tool

echo ""
echo "4. 🛑 Останавливаем сервер..."
pkill -f "uvicorn main:app"

echo "✅ Проверка завершена!"
