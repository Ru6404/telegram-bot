#!/bin/bash
echo "🔐 НАСТРОЙКА АВТОМАТИЧЕСКОЙ АВТОРИЗАЦИИ GITHUB"

# Проверяем установлен ли GH CLI
if ! command -v gh &> /dev/null; then
    echo "📦 Устанавливаем GitHub CLI..."
    
    # Для MacOS
    if [[ "$(uname)" == "Darwin" ]]; then
        brew install gh
    # Для Linux
    elif [[ -f /etc/debian_version ]]; then
        sudo apt update && sudo apt install -y gh
    elif [[ -f /etc/redhat-release ]]; then
        sudo dnf install -y gh
    else
        echo "❌ Не могу установить gh автоматически"
        exit 1
    fi
fi

# Авторизуемся в GitHub
echo "🔑 АВТОРИЗАЦИЯ В GITHUB..."
gh auth login --with-token <<< "ghp_твой_токен_здесь"

# Или альтернативный метод
setup_ssh_auto() {
    echo "🔐 НАСТРОЙКА SSH АВТОРИЗАЦИИ..."
    
    # Создаем SSH ключ если нет
    if [ ! -f ~/.ssh/id_ed25519 ]; then
        ssh-keygen -t ed25519 -C "ruslan6404kim@gmail.com" -f ~/.ssh/id_ed25519 -N ""
    fi
    
    # Добавляем ключ в агент
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_ed25519
    
    # Показываем публичный ключ для копирования в GitHub
    echo "📋 ДОБАВЬ ЭТОТ КЛЮЧ В GITHUB:"
    echo "https://github.com/settings/keys"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "⏳ Нажми Enter после добавления ключа..."
    read
}

# Меняем URL на SSH
echo "🌐 МЕНЯЕМ URL НА SSH..."
git remote set-url origin git@github.com:Ru6404/cloud-api.git

echo "✅ АВТОРИЗАЦИЯ НАСТРОЕНА!"
