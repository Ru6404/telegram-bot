#!/bin/bash
while true; do
    if ! pgrep -f "python quantum_bot.py" > /dev/null; then
        echo "$(date): Бот упал, перезапускаю..."
        python quantum_bot.py &
    fi
    sleep 30
done
