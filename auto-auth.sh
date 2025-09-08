#!/bin/bash
echo "🔐 АВТОМАТИЧЕСКАЯ АУТЕНТИФИКАЦИЯ GITHUB"

# Метод 1: Через личный токен (рекомендуется)
auth_with_token() {
    echo "🔑 Используем Personal Access Token"
    
    # Создаем файл с credentials
    git config --global credential.helper store
    echo "https://Ru6404:$1@github.com" > ~/.git-credentials
    chmod 600 ~/.git-credentials
    
    echo "✅ Токен сохранен"
}

# Метод 2: Через SSH
auth_with_ssh() {
    echo "🔑 Используем SSH"
    git remote set-url origin git@github.com:Ru6404/cloud-api.git
    echo "✅ Переключились на SSH"
}

# Метод 3: Через GH CLI
auth_with_gh() {
    echo "🔑 Используем GitHub CLI"
    if command -v gh &> /dev/null; then
        gh auth login --with-token <<< "$1" 2>/dev/null
        echo "✅ GitHub CLI авторизован"
    else
        echo "❌ GitHub CLI не установлен"
    fi
}

# Основная логика
main() {
    echo "🤖 Выбери метод аутентификации:"
    echo "1. Personal Access Token (рекомендуется)"
    echo "2. SSH ключи"
    echo "3. GitHub CLI"
    echo ""
    read -p "Введи номер (1-3): " choice
    
    case $choice in
        1)
            echo "📝 Получи токен здесь: https://github.com/settings/tokens"
            echo "📝 Нужны права: repo"
            read -p "Введи свой Personal Access Token: " token
            auth_with_token "$token"
            ;;
        2)
            auth_with_ssh
            ;;
        3)
            read -p "Введи токен для GitHub CLI: " token
            auth_with_gh "$token"
            ;;
        *)
            echo "❌ Неверный выбор"
            exit 1
            ;;
    esac
    
    # Тестируем подключение
    echo "🧪 Тестируем подключение..."
    if git ls-remote origin >/dev/null 2>&1; then
        echo "✅ Аутентификация успешна!"
    else
        echo "❌ Ошибка аутентификации"
    fi
}

main "$@"
