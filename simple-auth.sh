#!/bin/bash
echo "🔐 ПРОСТАЯ АУТЕНТИФИКАЦИЯ"

# Используем git credential helper
git config --global credential.helper 'cache --timeout=3600'

# Или сохраняем в store
git config --global credential.helper store

# Создаем файл с credentials
echo "https://Ru6404:ghp_твой_токен@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

# Тестируем
GIT_ASKPASS=echo git ls-remote origin
