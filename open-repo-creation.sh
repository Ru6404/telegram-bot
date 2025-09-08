#!/bin/bash
echo "🌐 ОТКРЫВАЕМ СТРАНИЦУ СОЗДАНИЯ РЕПОЗИТОРИЯ"

# Пытаемся открыть браузер
if command -v xdg-open > /dev/null; then
    xdg-open "https://github.com/new?name=auto-cloud-api&description=Auto-Cloud+API+deployment&public=true"
elif command -v open > /dev/null; then
    open "https://github.com/new?name=auto-cloud-api&description=Auto-Cloud+API+deployment&public=true"
else
    echo "📋 Открой вручную:"
    echo "https://github.com/new"
    echo ""
    echo "📝 Заполни:"
    echo "Name: auto-cloud-api"
    echo "Description: Auto-Cloud API deployment"
    echo "Public: ✓"
fi

echo "⏳ После создания репозитория вернись в терминал..."
