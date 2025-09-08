#!/bin/bash
echo "🔍 ПРОВЕРКА РЕПОЗИТОРИЯ auto-cloud-api"

# Проверяем оба варианта названий
REPOS=("auto-cloud-api" "cloud-api")

for repo in "${REPOS[@]}"; do
    echo "🔎 Проверяем $repo..."
    if curl -s https://api.github.com/repos/Ru6404/$repo | grep -q "Not Found"; then
        echo "❌ $repo - не существует"
    else
        echo "✅ $repo - существует!"
        echo "🌐 URL: https://github.com/Ru6404/$repo"
    fi
    echo ""
done

echo "📋 Текущий remote:"
git remote -v
