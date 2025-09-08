#!/bin/bash
# Скрипт для удаленной установки через одну команду

REMOTE_SCRIPT="https://raw.githubusercontent.com/Ru6404/cloud-api/main/universal-start.sh"

echo "🌐 Удаленная установка Cloud API..."
echo "📧 Для: ruslan6404kim@gmail.com"

# Скачиваем и запускаем скрипт
if command -v curl &> /dev/null; then
    curl -sSL "$REMOTE_SCRIPT" | bash
elif command -v wget &> /dev/null; then
    wget -qO - "$REMOTE_SCRIPT" | bash
else
    echo "❌ Установите curl или wget"
    exit 1
fi
