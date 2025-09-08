#!/bin/bash
echo "🔐 ПРАВИЛЬНОЕ ИСПОЛЬЗОВАНИЕ TOKEN"

# Загружаем .env
source ~/cloud-api/.env 2>/dev/null

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Токен не найден в .env"
    echo "📝 Создай токен с правами repo: https://github.com/settings/tokens"
    read -p "Введи токен: " GITHUB_TOKEN
    echo "GITHUB_TOKEN=$GITHUB_TOKEN" >> ~/cloud-api/.env
fi

# Используем специальный формат для HTTPS с токеном
git remote set-url origin https://Ru6404:${GITHUB_TOKEN}@github.com/Ru6404/cloud-api.git

echo "✅ Remote настроен с токеном"
echo "🧪 Тестируем..."
git ls-remote origin
