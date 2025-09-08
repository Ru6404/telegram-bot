#!/bin/bash
echo "🆕 СОЗДАНИЕ РЕПОЗИТОРИЯ AUTO-CLOUD-API"

REPO_NAME="auto-cloud-api"
GITHUB_URL="https://github.com/Ru6404/$REPO_NAME"

echo "📋 РЕПОЗИТОРИЙ: $REPO_NAME"
echo "🌐 БУДЕТ СОЗДАН: $GITHUB_URL"
echo ""

echo "📋 ИНСТРУКЦИЯ ДЛЯ СОЗДАНИЯ:"
echo "1. Открой: https://github.com/new"
echo "2. Заполни форму:"
echo "   - Owner: Ru6404"
echo "   - Repository name: auto-cloud-api"
echo "   - Description: Auto-Cloud API deployment"
echo "   - Выбери: Public"
echo "   - НЕ ставь галочку 'Add a README file'"
echo "   - НЕ добавляй .gitignore"
echo "   - НЕ добавляй лицензию"
echo "3. Нажми: 'Create repository'"
echo ""
echo "⏳ После создания репозитория нажми Enter здесь..."
read

# Проверяем создался ли репозиторий
echo "🔍 Проверяем создание репозитория..."
if curl -s https://api.github.com/repos/Ru6404/$REPO_NAME | grep -q "Not Found"; then
    echo "❌ Репозиторий еще не создан"
    echo "📋 Создай его вручную: https://github.com/new"
    exit 1
fi

echo "✅ Репозиторий создан! Настраиваем..."

# Настраиваем правильный remote
echo "🌐 Настраиваем remote URL..."
git remote remove origin 2>/dev/null
git remote add origin git@github.com:Ru6404/$REPO_NAME.git

echo "✅ Remote настроен: $(git remote get-url origin)"

# Добавляем все файлы
echo "📦 Добавляем файлы в git..."
git add .

# Создаем коммит
echo "💾 Создаем коммит..."
git commit -m "Initial commit: Auto-Cloud API with automatic deployment"

# Пушим
echo "📤 Пушим в GitHub..."
if git push -u origin main; then
    echo "🎉 УСПЕХ! РЕПОЗИТОРИЙ СОЗДАН И ЗАПУШЕН!"
    echo "🌐 Открой: $GITHUB_URL"
    echo "🚀 Приложение доступно по: https://Ru6404.github.io/$REPO_NAME/"
else
    echo "❌ Ошибка при push"
    echo "⚠️  Попробуй: git push -f origin
