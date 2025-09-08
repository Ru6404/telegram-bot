#!/bin/bash
echo "🔄 ВОССТАНОВЛЕНИЕ SSH КЛЮЧЕЙ ИЗ ENV"

# Загружаем env файл если есть
if [ -f ~/cloud-api/.env.ssh ]; then
    source ~/cloud-api/.env.ssh
fi

# Восстанавливаем приватный ключ
if [ -n "$GITHUB_SSH_PRIVATE_KEY" ]; then
    echo "🔑 Восстанавливаем приватный ключ..."
    mkdir -p ~/.ssh
    echo "$GITHUB_SSH_PRIVATE_KEY" | base64 -d > ~/.ssh/id_ed25519
    chmod 600 ~/.ssh/id_ed25519
fi

# Восстанавливаем публичный ключ
if [ -n "$GITHUB_SSH_PUBLIC_KEY" ]; then
    echo "🔑 Восстанавливаем публичный ключ..."
    echo "$GITHUB_SSH_PUBLIC_KEY" | base64 -d > ~/.ssh/id_ed25519.pub
    chmod 644 ~/.ssh/id_ed25519.pub
fi

# Добавляем ключ в ssh-agent
echo "🔐 Добавляем ключ в ssh-agent..."
eval "$(ssh-agent -s)" >/dev/null 2>&1
ssh-add ~/.ssh/id_ed25519 2>/dev/null

# Проверяем подключение
echo "🌐 Проверяем подключение к GitHub..."
ssh -T git@github.com
