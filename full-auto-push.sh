#!/bin/bash
echo "🤖 ПОЛНОСТЬЮ АВТОМАТИЧЕСКИЙ PUSH"

# Автоматически отвечаем yes на все вопросы SSH
echo "yes" | ssh -o StrictHostKeyChecking=accept-new -T git@github.com 2>&1

cd ~/cloud-api

# Добавляем все файлы
git add . 2>/dev/null

# Создаем коммит
git commit -m "Auto-push: $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null

# Пушим с автоматическим подтверждением
ssh -o StrictHostKeyChecking=accept-new git@github.com 2>&1
git push origin main 2>&1

echo "✅ Автоматический push завершен!"
