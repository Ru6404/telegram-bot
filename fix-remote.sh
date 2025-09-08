#!/bin/bash
echo "🔧 АВТОМАТИЧЕСКАЯ НАСТРОЙКА REMOTE"

# Проверяем существует ли репозиторий
echo "🔍 Проверяем репозиторий..."
if curl -s https://api.github.com/repos/Ru6404/cloud-api | grep -q "Not Found"; then
    echo "❌ Репозиторий не найден"
    exit 1
else
    echo "✅ Репозиторий существует: https://github.com/Ru6404/cloud-api"
fi

# Настраиваем правильный remote
echo "🌐 Настраиваем remote..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Ru6404/cloud-api.git

# Проверяем
echo "📋 Текущие remotes:"
git remote -v

echo "✅ Remote настроен правильно!"
