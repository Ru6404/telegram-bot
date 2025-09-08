#!/bin/bash
echo "🔐 АВТОМАТИЧЕСКАЯ НАСТРОЙКА SSH КЛЮЧА ДЛЯ GITHUB"

# Создаем SSH ключ если нет
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "📦 Создаем новый SSH ключ..."
    ssh-keygen -t ed25519 -C "ruslan6404kim@gmail.com" -f ~/.ssh/id_ed25519 -N ""
fi

# Добавляем ключ в ssh-agent
echo "🔑 Добавляем ключ в ssh-agent..."
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Показываем публичный ключ
echo "📋 КОПИРУЙ ЭТОТ КЛЮЧ И ДОБАВЬ В GITHUB:"
echo "https://github.com/settings/keys"
echo ""
cat ~/.ssh/id_ed25519.pub
echo ""
echo "🌐 Открой https://github.com/settings/keys в браузере"
echo "📌 Нажми 'New SSH key', вставь ключ выше и нажми 'Add SSH key'"
echo ""
echo "⏳ После добавления ключа нажми Enter здесь..."
read

# Проверяем подключение
echo "🔄 Проверяем подключение..."
ssh -T git@github.com

echo "✅ Настройка завершена!"
