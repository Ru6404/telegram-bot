#!/bin/bash
echo "🔧 ИСПРАВЛЯЕМ НАЗВАНИЕ РЕПОЗИТОРИЯ"

# Правильное название репозитория
CORRECT_REPO="auto-cloud-api"

# Проверяем существует ли репозиторий
echo "🔍 Проверяем репозиторий $CORRECT_REPO..."
if curl -s https://api.github.com/repos/Ru6404/$CORRECT_REPO | grep -q "Not Found"; then
    echo "❌ Репозиторий $CORRECT_REPO не существует"
    echo "📋 Создай его: https://github.com/new?name=$CORRECT_REPO"
    exit 1
else
    echo "✅ Репозиторий $CORRECT_REPO существует!"
fi

# Меняем remote URL
echo "🌐 Меняем remote на правильный..."
git remote remove origin 2>/dev/null
git remote add origin git@github.com:Ru6404/$CORRECT_REPO.git

echo "✅ Новый remote: $(git remote get-url origin)"

# Проверяем подключение
echo "🔗 Проверяем подключение..."
if git ls-remote origin >/dev/null 2>&1; then
    echo "✅ Подключение к репозиторию работает!"
    
    # Пушим
    echo "📤 Пушим код..."
    git push -u origin main
    
else
    echo "❌ Ошибка подключения"
    echo "📋 Проверь:"
    echo "1. SSH ключ добавлен в GitHub"
    echo "2. Ключ добавлен в ssh-agent"
    echo "3. Репозиторий существует: https://github.com/Ru6404/$CORRECT_REPO"
fi
