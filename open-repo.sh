#!/bin/bash
echo "🌐 ОТКРЫВАЕМ РЕПОЗИТОРИЙ НА GITHUB"

REPO_URL="https://github.com/Ru6404/auto-cloud-api"

echo "📋 Репозиторий: $REPO_URL"

# Пытаемся открыть в браузере
if command -v xdg-open > /dev/null; then
    xdg-open "$REPO_URL"
elif command -v open > /dev/null; then
    open "$REPO_URL"
else
    echo "📎 Открой вручную: $REPO_URL"
fi

echo "✅ Репозиторий должен быть доступен!"
