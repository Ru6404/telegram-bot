#!/bin/bash
# run_bot.sh - Скрипт автоматического перезапуска бота

cd ~/cloud-api

# Бесконечный цикл перезапуска
while true; do
    echo "🚀 Запускаем бота... ($(date))"
    python bot.py
    
    # Если бот упал, ждем 5 секунд и перезапускаем
    echo "⚠️ Бот остановился. Перезапуск через 5 секунд..."
    sleep 5
done
#!/data/data/com.termux/files/usr/bin/bash
# run_bot.sh - Скрипт запуска бота

cd /data/data/com.termux/files/home/cloud-api

echo "🤖 Запуск Telegram бота..."
echo "📅 Дата: $(date)"
echo "📂 Директория: $(pwd)"

# Бесконечный цикл с перезапуском
while true; do
    echo "🚀 Запускаем бота... ($(date))"
    python bot.py
    
    EXIT_CODE=$?
    echo "⚠️ Бот остановился с кодом: $EXIT_CODE"
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ Бот завершил работу нормально"
        break
    else
        echo "🔄 Перезапуск через 3 секунды..."
        sleep 3
    fi
done
