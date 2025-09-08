#!/bin/bash
# Автоматический push при изменении файлов

cd ~/cloud-api

while true; do
    # Проверяем изменения каждые 30 секунд
    if git status --porcelain | grep -q "."; then
        echo "🔄 Обнаружены изменения, пушим..."
        ./auto-push.sh
    fi
    sleep 30
done
