#!/bin/bash
echo "🚀 ПРИНУДИТЕЛЬНЫЙ PUSH В СУЩЕСТВУЮЩИЙ РЕПОЗИТОРИЙ"

# Настраиваем правильный remote
git remote remove origin 2>/dev/null
git remote add origin git@github.com:Ru6404/auto-cloud-api.git

echo "✅ Remote: $(git remote get-url origin)"

# Добавляем все файлы
echo "📦 Добавляем файлы..."
git add .

# Создаем коммит
echo "💾 Создаем коммит..."
git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"

# Принудительный push
echo "📤 Принудительный push..."
if git push -f origin main; then
    echo "🎉 УСПЕХ! Код запущен в существующий репозиторий!"
    echo "🌐 Открой: https://github.com/Ru6404/auto-cloud-api"
else
    echo "❌ Ошибка push"
    echo "🔍 Проверь доступ: ssh -T git@github.com"
fi
