#!/bin/bash
echo "🚀 DEPLOY НА RENDER.COM"

echo "📋 Инструкция для деплоя:"
echo "1. Открой: https://render.com"
echo "2. Нажми: 'New +' → 'Web Service'"
echo "3. Подключи GitHub аккаунт"
echo "4. Выбери репозиторий: Ru6404/auto-cloud-api"
echo "5. Настройки:"
echo "   - Name: auto-cloud-api"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "   - Plan: Free"
echo "6. Нажми: 'Create Web Service'"

echo ""
echo "⏳ После деплоя сайт будет доступен по ссылке вида:"
echo "   https://auto-cloud-api.onrender.com"
