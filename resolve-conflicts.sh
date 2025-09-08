#!/bin/bash
echo "⚡ РАЗРЕШЕНИЕ КОНФЛИКТОВ"

echo "📋 Если есть конфликты, сделай:"
echo "1. Посмотри конфликтующие файлы: git status"
echo "2. Отредактируй файлы, оставив нужные изменения"
echo "3. Добавь файлы: git add ."
echo "4. Продолжи rebase: git rebase --continue"
echo "5. Заверши: git push origin main"
echo ""
echo "🔄 Или отмени rebase и сделай force push:"
echo "git rebase --abort"
echo "git push -f origin main"
