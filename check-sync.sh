#!/bin/bash
echo "🔍 ПРОВЕРКА СИНХРОНИЗАЦИИ С GITHUB"

echo "📋 Локальная ветка main:"
git log --oneline -3

echo ""
echo "📋 Удаленная ветка main:"
git log --oneline origin/main -3

echo ""
echo "🔍 Сравнение:"
if git diff --quiet main origin/main; then
    echo "✅ Локальная и удаленная версии идентичны!"
    echo "🌐 Репозиторий: https://github.com/Ru6404/auto-cloud-api"
else
    echo "⚠️  Есть различия. Запусти: git pull origin main"
fi
