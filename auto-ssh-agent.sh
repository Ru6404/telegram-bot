#!/bin/bash
echo "🤖 АВТОМАТИЧЕСКИЙ ЗАПУСК SSH AGENT"

# Файл для хранения переменных агента
SSH_ENV="$HOME/.ssh/agent-environment"

# Запускаем агент если не запущен
start_agent() {
    echo "🔧 Инициализируем новый SSH agent..."
    ssh-agent | sed 's/^echo/#echo/' > "$SSH_ENV"
    chmod 600 "$SSH_ENV"
    . "$SSH_ENV" > /dev/null
    ssh-add ~/.ssh/id_ed25519
}

# Проверяем существует ли файл с переменными
if [ -f "$SSH_ENV" ]; then
    . "$SSH_ENV" > /dev/null
    # Проверяем что процесс еще жив
    if ps -p $SSH_AGENT_PID > /dev/null; then
        echo "✅ SSH Agent уже запущен: PID $SSH_AGENT_PID"
    else
        start_agent
    fi
else
    start_agent
fi

# Добавляем ключ
ssh-add ~/.ssh/id_ed25519 2>/dev/null

echo "🎯 Проверяем подключение..."
ssh -T git@github.com
 
