#!/bin/bash
echo "🚀 АВТОМАТИЧЕСКИЙ PUSH В GITHUB"

# Автоматически добавляем SSH host
mkdir -p ~/.ssh
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts 2>/dev/null

cd ~/cloud-api
#!/bin/bash
echo "🚀 АВТОМАТИЧЕСКИЙ PUSH В GITHUB"

cd ~/cloud-api

# Проверяем изменения
if git status --porcelain | grep -q "."; then
    echo "📦 Обнаружены изменения, добавляем в git..."
    git add .
    
    echo "💾 Создаем коммит..."
    git commit -m "Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo "📤 Пушим в GitHub..."
    if git push origin main; then
        echo "✅ УСПЕШНО ЗАПУШЕНО!"
    else
        echo "❌ ОШИБКА PUSH, пробуем через SSH..."
        git remote set-url origin git@github.com:Ru6404/cloud-api.git
        git push origin main
    fi
else
    echo "✅ Изменений нет"
fi
#!/bin/bash
echo "🚀 АВТОМАТИЧЕСКИЙ PUSH С ENV КЛЮЧАМИ"

# Загружаем SSH ключи из env
source ~/cloud-api/load-keys-from-env.sh

cd ~/cloud-api

# Настраиваем git
git config user.name "$GITHUB_USERNAME"
git config user.email "$GITHUB_EMAIL"
git remote set-url origin "$GITHUB_REPO"

# Добавляем файлы
git add . 2>/dev/null

# Создаем коммит
git commit -m "Auto-push: $(date '+%Y-%m-%d %H:%M:%S')" 2>/dev/null

# Пушим
if git push origin main; then
    echo "✅ УСПЕШНО ЗАПУШЕНО!"
else
    echo "❌ Ошибка push, проверяем SSH..."
    ./auto-ssh-setup.sh
    git push origin main
fi
