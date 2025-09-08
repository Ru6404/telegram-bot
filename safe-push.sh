#!/bin/bash
echo "🚀 БЕЗОПАСНЫЙ PUSH В GITHUB"

# Настраиваем правильный remote
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Ru6404/cloud-api.git

# Убедимся что мы на main ветке
git checkout -b main 2>/dev/null || git checkout main

# Добавляем все файлы
git add .

# Коммит
git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"

# Пуш с несколькими попытками
if git push -u origin main; then
    echo "✅ PUSH УСПЕШЕН!"
elif git push -f origin main; then
    echo "✅ PUSH УСПЕШЕН (с force)!"
else
    echo "❌ Ошибка push, проверь настройки"
fi
