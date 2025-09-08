#!/bin/bash
echo "🔐 ДОБАВЛЕНИЕ SSH КЛЮЧА В АГЕНТ"

# Запускаем ssh-agent
eval "$(ssh-agent -s)" >/dev/null 2>&1

# Добавляем ключ
ssh-add ~/.ssh/id_ed25519 2>/dev/null

# Проверяем что ключ добавлен
if ssh-add -l | grep -q "id_ed25519"; then
    echo "✅ Ключ добавлен в ssh-agent"
else
    echo "❌ Ошибка добавления ключа"
    echo "🔍 Проверь путь: ~/.ssh/id_ed25519"
    ls -la ~/.ssh/
fi

# Проверяем подключение
echo "🌐 Проверяем подключение к GitHub..."
ssh -T git@github.com
