#!/bin/bash
echo "🆕 АВТОМАТИЧЕСКОЕ СОЗДАНИЕ РЕПОЗИТОРИЯ"

# Проверяем существует ли репозиторий
if curl -s https://api.github.com/repos/Ru6404/cloud-api | grep -q "Not Found"; then
    echo "❌ Репозиторий не существует, создаем..."
    
    # Используем GitHub CLI если установлен
    if command -v gh &> /dev/null; then
        echo "🚀 Создаем репозиторий через GitHub CLI..."
        gh repo create Ru6404/cloud-api --public --description "Auto-Cloud API deployment" --confirm
    else
        echo "📋 ИНСТРУКЦИЯ ДЛЯ РУЧНОГО СОЗДАНИЯ:"
        echo "1. Открой: https://github.com/new"
        echo "2. Введи:"
        echo "   - Repository name: cloud-api"
        echo "   - Description: Auto-Cloud API deployment"
        echo "   - Public repository"
        echo "3. Нажми: 'Create repository'"
        echo ""
        echo "⏳ После создания репозитория нажми Enter..."
        read
    fi
else
    echo "✅ Репозиторий уже существует"
fi

# Настраиваем remote
echo "🌐 Настраиваем remote..."
git remote remove origin 2>/dev/null
git remote add origin git@github.com:Ru6404/cloud-api.git

echo "✅ Репозиторий настроен!"
