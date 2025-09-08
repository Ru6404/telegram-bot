#!/bin/bash
echo "🔍 ПРОВЕРКА И СОЗДАНИЕ РЕПОЗИТОРИЯ"

# Проверяем существует ли репозиторий
if curl -s https://api.github.com/repos/Ru6404/cloud-api | grep -q "Not Found"; then
    echo "❌ Репозиторий не найден, создаем..."
    ./create-repo.sh
else
    echo "✅ Репозиторий существует"
fi

# Инициализируем git если нужно
if [ ! -d .git ]; then
    echo "📦 Инициализируем git..."
    git init
    git config user.email "ruslan6404kim@gmail.com"
    git config user.name "Ru6404"
fi

# Добавляем remote
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Ru6404/cloud-api.git

echo "✅ Репозиторий настроен"
