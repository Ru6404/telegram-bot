#!/bin/bash
echo "💾 СОХРАНЕНИЕ SSH КЛЮЧЕЙ В ENV"

# Создаем директорию для ключей если нет
mkdir -p ~/.ssh

# Генерируем новый ключ если нет
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "🔑 Генерируем новый SSH ключ..."
    ssh-keygen -t ed25519 -C "ruslan6404kim@gmail.com" -f ~/.ssh/id_ed25519 -N ""
fi

# Сохраняем ключи в .env файл
cat > ~/cloud-api/.env.ssh << EOF
# SSH Keys for GitHub Auto-Deploy
export GITHUB_SSH_PRIVATE_KEY="$(cat ~/.ssh/id_ed25519 | base64 -w 0)"
export GITHUB_SSH_PUBLIC_KEY="$(cat ~/.ssh/id_ed25519.pub | base64 -w 0)"
export GITHUB_USERNAME="Ru6404"
export GITHUB_EMAIL="ruslan6404kim@gmail.com"
export GITHUB_REPO="git@github.com:Ru6404/cloud-api.git"
export SSH_KEY_PATH="$HOME/.ssh/id_ed25519"
EOF

echo "✅ Ключи сохранены в ~/cloud-api/.env.ssh"
echo "📋 Публичный ключ для GitHub:"
cat ~/.ssh/id_ed25519.pub
