#!/bin/bash
echo "🔄 АВТОМАТИЧЕСКАЯ СИНХРОНИЗАЦИЯ"

cd ~/cloud-api

# Тянем изменения с GitHub
echo "📥 Тянем изменения с GitHub..."
git pull origin main

# Пушим свои изменения
echo "📤 Пушим свои изменения..."
git add .
git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null
git push origin main 2>/dev/null

echo "✅ СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА!"
