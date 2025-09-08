#!/bin/bash
echo "🤖 НАСТРОЙКА GIT ASKPASS ИЗ .env"

# Создаем askpass скрипт
cat > ~/.git-askpass-env << 'EOF'
#!/bin/bash
# Загружаем .env
if [ -f ~/cloud-api/.env ]; then
    source ~/cloud-api/.env
fi

case "$1" in
    Username*) echo "Ru6404" ;;
    Password*) echo "$GITHUB_TOKEN" ;;
    *) exit 1 ;;
esac
EOF

chmod +x ~/.git-askpass-env

# Экспортируем для текущей сессии
export GIT_ASKPASS=~/.git-askpass-env

echo "✅ Askpass настроен из .env"
echo "🧪 Тестируем..."
git ls-remote origin
