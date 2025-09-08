#!/bin/bash
echo "🔍 ПРОВЕРКА РЕПОЗИТОРИЯ AUTO-CLOUD-API"

REPO="auto-cloud-api"
URL="https://github.com/Ru6404/$REPO"

echo "📋 Проверяем: $URL"

# Проверяем существует ли репозиторий
if curl -s https://api.github.com/repos/Ru6404/$REPO | grep -q "Not Found"; then
    echo "❌ Репозиторий $REPO не существует!"
    echo "📋 Создай его: https://github.com/new?name=$REPO"
else
    echo "✅ Репозиторий $REPO существует!"
    echo "🌐 Открой: $URL"
    
    # Проверяем доступ
    echo "🔐 Проверяем доступ..."
    if git ls-remote git@github.com:Ru6404/$REPO.git >/dev/null 2>&1; then
        echo "🎉 Доступ есть! Можно пушить."
    else
        echo "❌ Нет доступа к репозиторию"
        echo "📋 Добавь SSH ключ в GitHub:"
        cat ~/.ssh/id_ed25519.pub
        echo ""
        echo "🌐 https://github.com/settings/keys"
    fi
fi
