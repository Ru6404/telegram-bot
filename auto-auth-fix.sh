#!/bin/bash
echo "🤖 АВТОМАТИЧЕСКИЙ ВЫБОР МЕТОДА АУТЕНТИФИКАЦИИ"

# Пробуем SSH
echo "🔄 Пробуем SSH..."
git remote set-url origin git@github.com:Ru6404/cloud-api.git
if git ls-remote origin >/dev/null 2>&1; then
    echo "✅ SSH работает!"
    exit 0
fi

# Пробуем HTTPS с токеном
echo "🔄 Пробуем HTTPS с токеном..."
source ~/cloud-api/.env 2>/dev/null
if [ -n "$GITHUB_TOKEN" ]; then
    git remote set-url origin https://Ru6404:${GITHUB_TOKEN}@github.com/Ru6404/cloud-api.git
    if git ls-remote origin >/dev/null 2>&1; then
        echo "✅ HTTPS с токеном работает!"
        exit 0
    fi
fi

# Если ничего не работает - создаем SSH ключ
echo "🔑 Создаем SSH ключ..."
ssh-keygen -t ed25519 -C "ruslan6404kim@gmail.com" -f ~/.ssh/id_ed25519 -N ""

echo "📋 ДОБАВЬ КЛЮЧ В GITHUB:"
cat ~/.ssh/id_ed25519.pub
echo ""
echo "🌐 Открой: https://github.com/settings/keys"
echo "⏳ После добавления нажми Enter..."
read

# Тестируем
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com

echo "✅ Настройка завершена!"
