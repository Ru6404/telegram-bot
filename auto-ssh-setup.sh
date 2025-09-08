#!/bin/bash
echo "🔐 АВТОМАТИЧЕСКОЕ ПОДТВЕРЖДЕНИЕ SSH"

# Добавляем GitHub в known_hosts автоматически
mkdir -p ~/.ssh
touch ~/.ssh/known_hosts

# Добавляем fingerprint GitHub автоматически
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts

# Проверяем что добавилось
echo "✅ Добавлены fingerprints GitHub:"
grep github.com ~/.ssh/known_hosts

echo "🔄 Тестируем подключение..."
ssh -T git@github.com
#!/bin/bash
echo "🔐 АВТОМАТИЧЕСКАЯ НАСТРОЙКА SSH ДЛЯ GITHUB"

# Создаем SSH ключ если нет
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "📝 Создаем новый SSH ключ..."
    ssh-keygen -t ed25519 -C "ruslan6404kim@gmail.com" -f ~/.ssh/id_ed25519 -N "" -q
fi

# Добавляем ключ в ssh-agent
echo "🔑 Добавляем ключ в ssh-agent..."
eval "$(ssh-agent -s)" > /dev/null
ssh-add ~/.ssh/id_ed25519 2>/dev/null

# Добавляем GitHub в known_hosts
echo "🌐 Добавляем GitHub в known_hosts..."
mkdir -p ~/.ssh
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts 2>/dev/null

# Показываем публичный ключ для копирования
echo ""
echo "📋 КОПИРУЙ ЭТОТ КЛЮЧ И ДОБАВЬ В GITHUB:"
echo "https://github.com/settings/keys"
echo ""
cat ~/.ssh/id_ed25519.pub
echo ""
echo "⏳ После добавления ключа нажми Enter..."
read

# Проверяем подключение
echo "🔗 Проверяем подключение..."
ssh -T git@
#!/bin/bash
echo "🤖 АВТОМАТИЧЕСКАЯ НАСТРОЙКА SSH ИЗ ENV"

# Загружаем ключи из env
source ~/cloud-api/load-keys-from-env.sh

# Настраиваем git
git config --global user.name "$GITHUB_USERNAME"
git config --global user.email "$GITHUB_EMAIL"
git remote set-url origin "$GITHUB_REPO"

# Добавляем GitHub в known_hosts
mkdir -p ~/.ssh
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts 2>/dev/null

echo "✅ SSH настройка завершена!"
