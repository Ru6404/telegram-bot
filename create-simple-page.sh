#!/bin/bash
echo "📝 СОЗДАЕМ ПРОСТУЮ HTML СТРАНИЦУ"

# Создаем простую HTML страницу
cat > ~/cloud-api/templates/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Auto-Cloud API</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>🚀 Auto-Cloud API</h1>
    <p>Добро пожаловать в автоматическое облако!</p>
    
    <h2>📊 Статистика:</h2>
    <div id="stats">Загрузка...</div>
    
    <h2>🔗 Endpoints:</h2>
    <div class="endpoint">
        <strong>GET /</strong> - Главная страница (JSON)
    </div>
    <div class="endpoint">
        <strong>GET /health</strong> - Проверка здоровья
    </div>
    <div class="endpoint">
        <strong>GET /users</strong> - Список пользователей
    </div>
    <div class="endpoint">
        <strong>GET /todos</strong> - Список задач
    </div>

    <script>
        // Загружаем статистику
        fetch('/')
            .then(response => response.json())
            .then(data => {
                document.getElementById('stats').innerHTML = 
                    `👥 Пользователей: ${data.users}<br>` +
                    `✅ Задач: ${data.todos}<br>` +
                    `📝 Сообщение: ${data.message}`;
            });
    </script>
</body>
</html>
EOF

echo "✅ HTML страница создана: templates/index.html"
echo "🌐 После перезапуска сервера открой: http://localhost:8000/templates/index.html"
