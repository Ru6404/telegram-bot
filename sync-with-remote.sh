#!/bin/bash
echo "🔄 СИНХРОНИЗАЦИЯ С УДАЛЕННЫМ РЕПОЗИТОРИЕМ"

echo "📥 Тянем изменения из GitHub..."
if git pull --rebase origin main; then
    echo "✅ Изменения успешно получены"
    
    # Добавляем наши файлы
    echo "📦 Добавляем наши файлы..."
    git add .
    
    # Коммит
    echo "💾 Создаем коммит..."
    git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Пушим
    echo "📤 Пушим изменения..."
    if git push origin main; then
        echo "🎉 СИНХРОНИЗАЦИЯ УСПЕШНА!"
        echo "🌐 Репозиторий: https://github.com/Ru6404/auto-cloud-api"
    else
        echo "❌ Ошибка при push"
    fi
    
else
    echo "❌ Ошибка при pull"
    echo "📋 Попробуй вручную: git pull --rebase origin main"
fi
