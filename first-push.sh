#!/bin/bash
echo "🚀 ПЕРВЫЙ PUSH В НОВЫЙ РЕПОЗИТОРИЙ"

# Создаем репозиторий если нужно
./init-repo.sh

# Добавляем все файлы
git add .

# Создаем первый коммит
git commit -m "Initial commit: Auto-Cloud API"

# Пушим с созданием ветки main
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ ПЕРВЫЙ PUSH УСПЕШЕН!"
    echo "🌐 Репозиторий: https://github.com/Ru6404/cloud-api"
else
    echo "❌ Ошибка push, пробуем с force..."
    git push -f origin main
fi
#!/bin/bash
echo "🚀 ПЕРВЫЙ PUSH В НОВЫЙ РЕПОЗИТОРИЙ"

# Создаем репозиторий если нужно
~/cloud-api/create-repo-auto.sh

# Убедимся что мы на правильной ветке
git branch -M main 2>/dev/null

# Добавляем все файлы
echo "📦 Добавляем файлы..."
git add .

# Создаем первый коммит
echo "💾 Создаем коммит..."
git commit -m "Initial commit: Auto-Cloud API with auto-deployment"

# Пушим
echo "📤 Пушим в GitHub..."
if git push -u origin main; then
    echo "✅ ПЕРВЫЙ PUSH УСПЕШЕН!"
    echo "🌐 Репозиторий: https://github.com/Ru6404/cloud-api"
else
    echo "❌ Ошибка push, пробуем с force..."
    git push -f origin main
fi
