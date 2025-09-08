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
