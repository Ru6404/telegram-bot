#!/bin/bash
echo "🎯 СОЗДАНИЕ GITHUB TOKEN"

echo "📋 ИНСТРУКЦИЯ:"
echo "1. Открой: https://github.com/settings/tokens"
echo "2. Нажми: 'Generate new token'"
echo "3. Выбери: 'repo' права"
echo "4. Скопируй токен и вставь ниже"
echo ""
echo "💡 Совет: Назови токен 'Cloud-API-Auto-Deploy'"
echo ""

read -p "Нажми Enter чтобы открыть браузер... "
# Открываем браузер с ссылкой
if [[ "$(uname)" == "Darwin" ]]; then
    open "https://github.com/settings/tokens"
elif command -v xdg-open &> /dev/null; then
    xdg-open "https://github.com/settings/tokens"
else
    echo "📎 Открой вручную: https://github.com/settings/tokens"
fi

read -p "📝 Введи свой GitHub токен: " token

# Сохраняем токен
echo "$token" > ~/.github_token
chmod 600 ~/.github_token
echo "export GITHUB_TOKEN='$token'" >> ~/cloud-api/.env
echo "✅ Токен сохранен в ~/.github_token"

# Настраиваем git
git config --global credential.helper "store --file ~/.git-credentials"
echo "https://Ru6404:$token@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

echo "✅ Аутентификация настроена!"
