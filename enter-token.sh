#!/bin/bash
echo "🔑 ВВЕДИ GITHUB TOKEN"

echo "📝 Получи токен здесь: https://github.com/settings/tokens"
echo "💡 Нужны права: repo"
echo ""

read -p "Введи свой GitHub Token: " token

# Сохраняем токен для автоматического использования
echo "https://Ru6404:$token@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

# Настраиваем git для использования store
git config --global credential.helper store

echo "✅ Токен сохранен. Пробуем аутентификацию..."
git ls-remote originv
