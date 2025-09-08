#!/bin/bash
echo "🚀 PUSH С АВТОАУТЕНТИФИКАЦИЕЙ"

# Пробуем разные методы аутентификации
try_push() {
    echo "🔄 Пробуем метод: $1"
    
    if git push -u origin main; then
        echo "✅ PUSH УСПЕШЕН!"
        return 0
    fi
    return 1
}

# Метод 1: Через сохраненный токен
if [ -f ~/.github_token ]; then
    token=$(cat ~/.github_token)
    git config --global credential.helper "store --file ~/.git-credentials"
    echo "https://Ru6404:$token@github.com" > ~/.git-credentials
    try_push "Saved Token"
fi

# Метод 2: Через SSH
if ! try_push "SSH"; then
    git remote set-url origin git@github.com:Ru6404/cloud-api.git
    try_push "SSH"
fi

# Метод 3: Через интерактивный ввод
if ! try_push "Interactive"; then
    echo "🔑 Введи логин и пароль вручную:"
    git push -u origin main
fi

echo "🎉 Готово!"
