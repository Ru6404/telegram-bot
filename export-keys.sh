#!/bin/bash
echo "📤 ЭКСПОРТ SSH КЛЮЧЕЙ"

if [ -f ~/cloud-api/.env.ssh ]; then
    echo "🔑 Privat Key (base64):"
    grep GITHUB_SSH_PRIVATE_KEY ~/cloud-api/.env.ssh | cut -d'"' -f2
    
    echo ""
    echo "🔑 Public Key (для GitHub):"
    grep GITHUB_SSH_PUBLIC_KEY ~/cloud-api/.env.ssh | cut -d'"' -f2 | base64 -d
    
    echo ""
    echo "🌐 GitHub Repo: $GITHUB_REPO"
else
    echo "❌ .env.ssh файл не найден"
    ./save-keys-to-env.sh
fi
