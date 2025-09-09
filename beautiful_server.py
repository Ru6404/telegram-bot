from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import time

app = FastAPI()

# Красивый HTML интерфейс
HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum System 2025 🚀</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: white; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        
        .header { 
            text-align: center; 
            padding: 2rem; 
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            margin-bottom: 2rem;
        }
        .logo { font-size: 4rem; margin-bottom: 1rem; }
        .title { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .subtitle { font-size: 1.2rem; opacity: 0.9; }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .card h3 { 
            margin-bottom: 1rem; 
            display: flex; 
            align-items: center;
            gap: 0.5rem;
        }
        
        .user-item, .task-item {
            padding: 0.8rem;
            margin: 0.5rem 0;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }
        
        .status {
            display: inline-block;
            padding: 0.2rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            margin-left: 0.5rem;
        }
        .online { background: #4ade80; color: black; }
        .offline { background: #ff4757; color: white; }
        .completed { background: #4ade80; color: black; }
        .progress { background: #fbbf24; color: black; }
        .pending { background: #94a3b8; color: white; }
        
        .api-info {
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .btn {
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin: 0.5rem;
            transition: all 0.3s ease;
        }
        .btn:hover { background: rgba(255, 255, 255, 0.3); transform: translateY(-2px); }
        
        .footer {
            text-align: center;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡</div>
            <h1 class="title">Quantum System 2025</h1>
            <p class="subtitle">Универсальная AI система</p>
        </div>
        
        <div class="dashboard">
            <!-- Пользователи -->
            <div class="card">
                <h3>👥 Пользователи</h3>
                <div class="user-item">
                    <strong>Администратор</strong>
                    <span class="status online">online</span>
                </div>
                <div class="user-item">
                    <strong>Разработчик</strong>
                    <span class="status online">online</span>
                </div>
                <div class="user-item">
                    <strong>Тестировщик</strong>
                    <span class="status offline">offline</span>
                </div>
            </div>
            
            <!-- Задачи -->
            <div class="card">
                <h3>📋 Задачи</h3>
                <div class="task-item">
                    <strong>Развертывание системы</strong>
                    <span class="status completed">completed</span>
                </div>
                <div class="task-item">
                    <strong>Интеграция Telegram</strong>
                    <span class="status progress">in progress</span>
                </div>
                <div class="task-item">
                    <strong>Оптимизация API</strong>
                    <span class="status pending">pending</span>
                </div>
            </div>
            
            <!-- Статус системы -->
            <div class="card">
                <h3>🌐 Статус системы</h3>
                <div class="api-info">
                    <strong>Статус:</strong> <span class="status online">online</span><br>
                    <strong>Версия:</strong> 2025.1.0<br>
                    <strong>Порт:</strong> 8080<br>
                    <strong>Время работы:</strong> <span id="uptime">0</span> сек
                </div>
                
                <div style="text-align: center;">
                    <a href="/health" class="btn">📊 Статус API</a>
                    <a href="/api" class="btn">🔧 API информация</a>
                </div>
            </div>
            
            <!-- Документы -->
            <div class="card">
                <h3>📁 Документы</h3>
                <div class="user-item">
                    <strong>Техническая документация</strong><br>
                    <small>PDF, 2.5MB</small>
                </div>
                <div class="user-item">
                    <strong>API руководство</strong><br>
                    <small>MD, 1.2MB</small>
                </div>
                <div class="user-item">
                    <strong>Установка и настройка</strong><br>
                    <small>DOC, 3.1MB</small>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 Quantum System | Все системы работают стабильно 🚀</p>
        </div>
    </div>
    
    <script>
        // Аптайм системы
        let startTime = Date.now();
        function updateUptime() {
            const uptime = Math.floor((Date.now() - startTime) / 1000);
            document.getElementById('uptime').textContent = uptime;
        }
        setInterval(updateUptime, 1000);
        
        // Автообновление статуса
        async function checkStatus() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                console.log('Система онлайн:', data.status);
            } catch (error) {
                console.error('Ошибка подключения:', error);
            }
        }
        setInterval(checkStatus, 30000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(HTML)

@app.get("/health")
async def health():
    return JSONResponse({
        "status": "healthy", 
        "version": "2025.1.0",
        "timestamp": time.time(),
        "server": "Quantum System 2025"
    })

@app.get("/api")
async def api_info():
    return JSONResponse({
        "endpoints": {
            "/": "Главная страница с интерфейсом",
            "/health": "Статус системы",
            "/api": "Информация о API"
        }
    })

if __name__ == "__main__":
    print("🚀 Запускаем красивый Quantum Server...")
    print("🌐 Откройте: http://127.0.0.1:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
