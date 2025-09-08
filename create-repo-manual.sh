#!/bin/bash
echo "🛠️ СОЗДАНИЕ РЕПОЗИТОРИЯ ВРУЧНУЮ"

echo "📋 ИНСТРУКЦИЯ:"
echo "1. Открой: https://github.com/new"
echo "2. Введи:"
echo "   - Repository name: cloud-api"
echo "   - Description: Auto-Cloud API deployment"
echo "   - Public repository"
echo "3. Нажми: 'Create repository'"
echo "4. Скопируй URL репозитория"
echo ""
echo "📝 Введи URL репозитория (https://github.com/Ru6404/cloud-api.git):"
read -r REPO_URL

# Настраиваем git
git init
git config user.email "ruslan6404kim@gmail.com"
git config user.name "Ru6404"
git remote add origin "$REPO_URL"

echo "✅ Репозиторий настроен!"
