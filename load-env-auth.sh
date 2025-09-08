#!/bin/bash
echo "🔐 АВТОЗАГРУЗКА АУТЕНТИФИКАЦИИ"

if [ -f ~/cloud-api/.env ]; then
    source ~/cloud-api/.env
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "✅ Загружен токен из .env"
        git config --global credential.helper "store --file ~/.git-credentials"
        echo "https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com" > ~/.git-credentials
        chmod 600 ~/.git-credentials
    fi
fi

# Проверяем аутентификацию
if git ls-remote origin >/dev/null 2>&1; then
    echo "✅ Аутентификация успешна"
else
    echo "❌ Требуется настройка аутентификации"
    ./auto-auth.sh
fi
