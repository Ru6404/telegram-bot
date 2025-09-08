#!/bin/bash
echo "🔐 ПРОВЕРКА ДОСТУПА К РЕПОЗИТОРИЮ"

echo "1. Проверяем SSH подключение к GitHub..."
ssh -T git@github.com

echo ""
echo "2. Проверяем доступ к репозиторию..."
curl -s -I https://api.github.com/repos/Ru6404/auto-cloud-api | head -1

echo ""
echo "3. Проверяем текущий remote:"
git remote -v

echo ""
echo "4. Проверяем SSH ключи:"
ssh-add -l

echo ""
echo "5. Пытаемся получить информацию о репозитории:"
curl -s https://api.github.com/repos/Ru6404/auto-cloud-api | grep -E '"name"|"private"|"html_url"'
