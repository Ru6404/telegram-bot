#!/bin/bash
echo "🔐 ЗАПУСК SSH AGENT"

# Проверяем запущен ли агент
if [ -z "$SSH_AGENT_PID" ]; then
    echo "🚀 Запускаем ssh-agent..."
    eval "$(ssh-agent -s)"
    echo "✅ SSH Agent запущен: PID $SSH_AGENT_PID"
else
    echo "✅ SSH Agent уже запущен: PID $SSH_AGENT_PID"
fi

# Добавляем ключ
echo "🔑 Добавляем SSH ключ..."
ssh-add ~/.ssh/id_ed25519

# Проверяем
echo "📋 Добавленные ключи:"
ssh-add -l

# Проверяем подключение
echo "🌐 Проверяем подключение к GitHub..."
ssh -T git@github.com
