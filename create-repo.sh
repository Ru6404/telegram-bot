#!/bin/bash
echo "🆕 СОЗДАНИЕ РЕПОЗИТОРИЯ НА GITHUB"

# Проверяем установлен ли gh
if ! command -v gh &> /dev/null; then
    echo "📦 Устанавливаем GitHub CLI..."
    if [[ "$(uname)" == "Darwin" ]]; then
        brew install gh
    else
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null
        sudo apt update
        sudo apt install -y gh
    fi
fi

# Авторизуемся в GitHub
echo "🔐 АВТОРИЗАЦИЯ В GITHUB..."
gh auth login --with-token <<< "ghp_твой_токен" 2>/dev/null || echo "⚠️ Используем существующую авторизацию"

# Создаем репозиторий
echo "🆕 СОЗДА
