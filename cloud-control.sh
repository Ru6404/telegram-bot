#!/bin/bash
case "$1" in
    start)
        cd ~/cloud-api
        python -m uvicorn main:app --reload &
        echo "✅ Сервер запущен"
        ;;
    stop)
        pkill -f "uvicorn main:app"
        echo "✅ Сервер остановлен"
        ;;
    status)
        if pgrep -f "uvicorn main:app" > /dev/null; then
            echo "✅ Сервер запущен"
            curl -s http://localhost:8000/health
        else
            echo "❌ Сервер не запущен"
        fi
        ;;
    restart)
        pkill -f "uvicorn main:app"
        sleep 2
        cd ~/cloud-api
        python -m uvicorn main:app --reload &
        echo "✅ Сервер перезапущен"
        ;;
    *)
        echo "Использование: cloud-control {start|stop|status|restart}"
        ;;
esac
