#!/bin/bash
echo "🔐 ИСПОЛЬЗУЕМ ТОКЕН ИЗ .env"

# Загружаем .env если есть
if [ -f ~/cloud-api/.env ]; then
    source ~/cloud-api/.env
    echo "✅ .env загружен"
    echo "📝 Токен: ${GITHUB_TOKEN:0:10}..."  # Показываем только первые 10 символов
else
    echo "❌ .env файл не найден"
    exit 1
fi

# Настраиваем git для использования токена
echo "🌐 НАСТРАИВАЕМ GIT..."
git config --global credential.helper 'store --file ~/.git-credentials'
echo "https://Ru6404:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

echo "✅ Токен из .env применен!"
