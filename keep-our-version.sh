#!/bin/bash
echo "🤖 ОСТАВЛЯЕМ НАШУ ВЕРСИЮ ФАЙЛОВ"

# Отменяем текущий rebase
git rebase --abort

# Используем нашу версию всех файлов
echo "📦 Используем нашу версию файлов..."
git checkout --ours .

# Добавляем все файлы
git add .

# Создаем коммит
git commit -m "Use our version: resolve merge conflicts"

# Force push
echo "📤 Force push..."
git push -f origin main

echo "✅ Наша версия файлов сохранена!"
