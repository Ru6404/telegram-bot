#!/bin/bash
echo "🎯 АВТОМАТИЗАЦИЯ АУТЕНТИФИКАЦИИ С EXPECT"

# Проверяем установлен ли expect
if ! command -v expect &> /dev/null; then
    echo "📦 Устанавливаем expect..."
    if [[ "$(uname)" == "Darwin" ]]; then
        brew install expect
    else
        sudo apt-get install -y expect
    fi
fi

# Создаем expect скрипт
cat > /tmp/git-auth.expect << 'EOF'
#!/usr/bin/expect -f
set timeout 20

spawn git ls-remote origin

expect "Username for 'https://github.com':"
send "Ru6404\r"

expect "Password for 'https://Ru6404@github.com':"
send "ghp_твой_токен_здесь\r"

expect eof
EOF

# Запускаем expect
chmod +x /tmp/git-auth.expect
/tmp/git-auth.expect

echo "✅ Аутентификация завершена"
