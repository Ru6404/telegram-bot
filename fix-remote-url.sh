#!/bin/bash
echo "🔧 ИСПРАВЛЯЕМ REMOTE URL"

# Правильное название репозитория
CORRECT_REPO="auto-cloud-api"
CORRECT_URL="git@github.com:Ru6404/$CORRECT_REPO.git"

echo "📋 Меняем remote на: $CORRECT_URL"

# Удаляем старый remote
git remote remove origin 2>/dev/null

# Добавляем правильный remote
git remote add origin "$CORRECT_URL"

echo "✅ Новый remote:"
git remote -v

# Проверяем подключение
echo "🔗 Проверяем подключение к правильному репозиторию..."
if git ls-remote origin >/dev/null 2>&1; then
    echo "🎉 УСПЕХ! Подключение к auto-cloud-api работает!"
    
    # Пушим код
    echo "📤 Пушим код в auto-cloud-api..."
    git push -u origin main
    
else
    echo "❌ Ошибка подключения к auto-cloud-api"
    echo "📋 Проверь:"
    echo "1. Репозиторий существует: https://github.com/Ru6404/auto-cloud-api"
    echo "2. SSH ключ добавлен в GitHub"
    echo "3. Ключ в агенте: ssh-add -l"
fi
