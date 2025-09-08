#!/bin/bash
echo "📦 УСТАНОВКА GITHUB CLI"

if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI уже установлен"
else
    echo "🚀 Устанавливаем GitHub CLI..."
    
    if [[ "$(uname -m)" == "aarch64" ]]; then
        # Для Termux на Android
        pkg install gh
    elif [[ "$(uname)" == "Darwin" ]]; then
        # Для MacOS
        brew install gh
    else
        # Для Linux
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install -y gh
    fi
    
    echo "✅ GitHub CLI установлен"
fi

# Авторизуемся
echo "🔐 Авторизуемся в GitHub..."
gh auth login --with-token <<< "ghp_твой_токен" 2>/dev/null || echo "⚠️ Требуется ручная авторизация"
