#!/bin/bash
echo "🤖 АВТОМАТИЧЕСКАЯ НАСТРОЙКА CREDENTIALS"

# Создаем скрипт для автоматического ответа
cat > ~/.git-askpass << 'EOF'
#!/bin/bash
case "$1" in
    Username*) echo "Ru6404" ;;
    Password*) cat ~/.github_token 2>/dev/null || echo "ghp_твой_токен" ;;
    *) exit 1 ;;
esac
EOF

chmod +x ~/.git-askpass

# Экспортируем для текущей сессии
export GIT_ASKPASS=~/.git-askpass

echo "✅ Askpass настроен. Тестируем..."
git ls-remote origin
