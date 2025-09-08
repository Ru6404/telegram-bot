#!/bin/bash
echo "🔐 ПЕРЕКЛЮЧЕНИЕ НА SSH АУТЕНТИФИКАЦИЮ"

# Меняем remote URL на SSH
git remote set-url origin git@github.com:Ru6404/cloud-api.git

echo "✅ Remote переключен на SSH"
echo "🌐 Новый URL: $(git remote get-url origin)"

# Проверяем SSH ключи
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "🔑 Создаем SSH ключ..."
    ssh-keygen -t ed25519 -C "ruslan6404kim@gmail.com" -f ~/.ssh/id_ed25519 -N ""
fi

# Добавляем ключ в агент
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

echo "📋 ДОБАВЬ ЭТОТ КЛЮЧ В GITHUB:"
echo "https://github.com/settings/keys"
cat ~/.ssh/id_ed25519.pub
echo ""
echo "⏳ После добавления ключа нажми Enter..."
read

echo "🧪 Тестируем подключение..."
ssh -T git@github.com
