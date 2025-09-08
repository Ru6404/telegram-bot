#!/bin/bash
echo "🤖 ПОЛНАЯ НАСТРОЙКА SSH ИЗ .env"

# Восстанавливаем ключи из .env
~/cloud-api/create-ssh-from-env.sh

# Добавляем ключ в агент
~/cloud-api/add-ssh-to-agent.sh

# Добавляем GitHub в known_hosts
echo "🔐 Добавляем GitHub в known_hosts..."
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts 2>/dev/null

# Проверяем финальное подключение
echo "🎯 Финальная проверка..."
if ssh -T git@github.com 2>&1 | grep -q "successfully"; then
    echo "✅ SSH НАСТРОЕН УСПЕШНО!"
    echo "🚀 Теперь можно пушить: git push origin main"
else
    echo "❌ Ошибка SSH подключения"
    echo "📋 Убедись что ключ добавлен в GitHub:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "🌐 https://github.com/settings/keys"
fi
