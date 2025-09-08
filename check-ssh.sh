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
#!/bin/bash
echo "🔍 ПРОВЕРКА SSH КЛЮЧА"

# Проверяем существует ли ключ
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "❌ SSH ключ не найден"
    exit 1
fi

# Проверяем добавлен ли в агент
if ! ssh-add -l | grep -q "id_ed25519"; then
    echo "🔑 Добавляем ключ в агент..."
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
fi

# Проверяем подключение
echo "🌐 Проверяем подключение к GitHub..."
ssh -T git@github.com

if [ $? -eq 0 ]; then
    echo "✅ SSH подключение работает!"
else
    echo "❌ SSH не настроен"
    echo "📋 Убедись что ключ добавлен в GitHub:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "🌐 https://github.com/settings/keys"
fi
