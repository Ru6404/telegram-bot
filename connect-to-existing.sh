#!/bin/bash
echo "🔗 ПОДКЛЮЧЕНИЕ К СУЩЕСТВУЮЩЕМУ РЕПОЗИТОРИЮ"

REPO_NAME="auto-cloud-api"
REPO_URL="https://github.com/Ru6404/$REPO_NAME"

echo "📋 Репозиторий: $REPO_NAME"
echo "🌐 URL: $REPO_URL"

# Проверяем существование репозитория
echo "🔍 Проверяем существование репозитория..."
if curl -s https://api.github.com/repos/Ru6404/$REPO_NAME | grep -q "Not Found"; then
    echo "❌ Репозиторий не существует"
    exit 1
else
    echo "✅ Репозиторий существует!"
fi

# Настраиваем правильный remote
echo "🌐 Настраиваем remote URL..."
git remote remove origin 2>/dev/null
git remote add origin git@github.com:Ru6404/$REPO_NAME.git

echo "✅ Remote настроен: $(git remote get-url origin)"

# Проверяем подключение
echo "🔗 Проверяем подключение..."
if git ls-remote origin >/dev/null 2>&1; then
    echo "✅ Подключение работает!"
    
    # Синхронизируем с удаленным репозиторием
    echo "🔄 Синхронизируем с GitHub..."
    git fetch origin
    
    # Проверяем есть ли различия
    if git diff --quiet main origin/main 2>/dev/null; then
        echo "✅ Локальная и удаленная версии идентичны"
    else
        echo "⚠️  Есть различия между локальной и удаленной версией"
        echo "📦 Пушим изменения..."
        git push -u origin main
    fi
    
else
    echo "❌ Ошибка подключения"
    echo "📋 Возможные причины:"
    echo "1. Нет доступа к репозиторию"
    echo "2. SSH ключ не добавлен в GitHub"
    echo "3. SSH ключ не добавлен в агент"
    echo ""
    echo "🔍 Проверь: ssh -T git@github.com"
fi
