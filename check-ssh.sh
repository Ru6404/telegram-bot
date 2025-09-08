#!/bin/bash
echo "🔍 ПРОВЕРКА SSH ПОДКЛЮЧЕНИЯ"

# Проверяем есть ли ключ
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "❌ SSH ключ не найден"
    exit 1
fi

# Проверяем добавлен ли ключ в агент
if ! ssh-add -l | grep -q "id_ed25519"; then
    echo "🔑 Добавляем ключ в агент..."
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
fi

# Проверяем подключение к GitHub
echo "🌐 Проверяем подключение к GitHub..."
ssh -T git@github.com
