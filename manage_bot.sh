#!/data/data/com.termux/files/usr/bin/bash
# manage_bot.sh - Управление ботом

BOT_PID_FILE="bot.pid"
LOG_FILE="bot.log"

case "$1" in
    start)
        echo "🚀 Запуск бота..."
        nohup ./run_bot.sh >> $LOG_FILE 2>&1 &
        echo $! > $BOT_PID_FILE
        echo "✅ Бот запущен. PID: $(cat $BOT_PID_FILE)"
        echo "📋 Логи: tail -f $LOG_FILE"
        ;;
    stop)
        if [ -f $BOT_PID_FILE ]; then
            BOT_PID=$(cat $BOT_PID_FILE)
            echo "⏹️ Остановка бота (PID: $BOT_PID)..."
            kill $BOT_PID 2>/dev/null
            rm -f $BOT_PID_FILE
            echo "✅ Бот остановлен"
        else
            echo "❌ Файл PID не найден. Останавливаем все процессы Python..."
            pkill -f "python bot.py"
        fi
        ;;
    status)
        if [ -f $BOT_PID_FILE ]; then
            BOT_PID=$(cat $BOT_PID_FILE)
            if ps -p $BOT_PID > /dev/null; then
                echo "✅ Бот работает (PID: $BOT_PID)"
            else
                echo "❌ Бот не работает (PID файл есть, но процесс умер)"
                rm -f $BOT_PID_FILE
            fi
        else
            echo "❌ Бот не запущен"
        fi
        ;;
    logs)
        echo "📋 Просмотр логов:"
        if [ -f $LOG_FILE ]; then
            tail -f $LOG_FILE
        else
            echo "📝 Лог-файл не найден. Создаем новый..."
            touch $LOG_FILE
            tail -f $LOG_FILE
        fi
        ;;
    restart)
        echo "🔄 Перезапуск бота..."
        ./manage_bot.sh stop
        sleep 2
        ./manage_bot.sh start
        ;;
    *)
        echo "🤖 Управление Telegram ботом"
        echo "Использование: ./manage_bot.sh {start|stop|status|logs|restart}"
        echo ""
        echo "  start    - Запустить бота"
        echo "  stop     - Остановить бота"
        echo "  status   - Статус бота"
        echo "  logs     - Просмотр логов"
        echo "  restart  - Перезапустить бота"
        ;;
esac
