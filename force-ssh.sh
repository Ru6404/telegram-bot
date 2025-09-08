#!/bin/bash
echo "🔐 ПРИНУДИТЕЛЬНОЕ ПЕРЕКЛЮЧЕНИЕ НА SSH"

# Удаляем старый remote
git remote remove origin 2>/dev/null

# Добавляем SSH remote
git remote add origin git@github.com:Ru6404/cloud-api.git

echo "✅ Remote переключен на SSH"
echo "🌐 Новый URL: $(git remote get-url origin)"

# Проверяем SSH подключение
echo "🧪 Проверяем SSH ключи..."
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "🔑 Создаем SSH ключ..."
    ssh-keygen -t ed25519 -C "ruslan6404kim@gmail.com" -f ~/.ssh/id_ed25519 -N ""
fi

# Добавляем ключ в агент
eval "$(ssh-agent -s)" >/dev/null 2>&1
ssh-add ~/.ssh/id_ed25519 2>/dev/null

echo "📋 Публичный ключ для GitHub:"
cat ~/.ssh/id_ed25519.pub
echo ""
echo "🌐 Добавь этот ключ здесь: https://github.com/settings/keys"
echo "⏳ После добавления нажми Enter..."
read

echo "🔗 Тестируем подключение к GitHub..."
ssh -T git@github.com
