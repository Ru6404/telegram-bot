#!/bin/bash
echo "🔑 НАСТРОЙКА GITHUB TOKEN"

echo "📋 ИНСТРУКЦИЯ:"
echo "1. Открой: https://github.com/settings/tokens"
echo "2. Нажми: 'Generate new token'"
echo "3. Выбери: 'repo' права"
echo "4. Скопируй токен и вставь ниже"
echo ""
echo "📝 Введи свой GitHub токен:"
read -r GITHUB_TOKEN

# Сохраняем токен в env
echo "export GITHUB_TOKEN='$GITHUB_TOKEN'" >> ~/cloud-api/.env.ssh
echo "✅ Токен сохранен в .env.ssh"
