#!/bin/bash
echo "🔍 ПРОВЕРКА И НАСТРОЙКА АУТЕНТИФИКАЦИИ"

# Проверяем есть ли .env
if [ ! -f ~/cloud-api/.env ]; then
    echo "❌ .env файл не найден"
    echo "📝 Создаем базовый .env..."
    cat > ~/cloud-api/.env << EOF
GITHUB_USERNAME=Ru6404
GITHUB_TOKEN=ghp_твой_токен_здесь
GITHUB_EMAIL=ruslan6404kim@gmail.com
EOF
    echo "✅ .env создан, отредактируй его и добавь токен"
    exit 1
fi

# Загружаем .env
source ~/cloud-api/.env

# Проверяем есть ли токен
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN не найден в .env"
    echo "📝 Добавь в ~/cloud-api/.env:"
    echo "GITHUB_TOKEN=ghp_твой_действительный_токен"
    exit 1
fi

echo "✅ Токен найден в .env"

# Настраиваем git
echo "🔧 Настраиваем git credentials..."
git config --global credential.helper store
echo "https://Ru6404:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

echo "🎯 Тестируем аутентификацию..."
git ls-remote origin
