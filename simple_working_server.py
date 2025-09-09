from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import socket
import time

app = FastAPI(title="Quantum Working System")

# Простой HTML без шаблонов
HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum System 🚀</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; padding: 20px; color: white; min-height: 100vh;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { text-align: center; padding: 2rem; }
        .logo { font-size: 3rem; }
        .title { font-size: 2rem; margin: 1rem 0; }
        
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 1rem; 
            margin: 2rem 0; 
        }
        
        .card {
            background: rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .card h3 { margin-top: 0; }
        .status { color: #4ade80; font-weight: bold; }
        
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡</div>
            <h1 class="title">Quantum System 2025</h1>
            <p>Работает на порту: <span class="status" id="port">8080</span></p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>👥 Пользователи</h3>
                <p>• Администратор <span class="status">online</span></p>
                <p>• Разработчик <span class="status">online</span></p>
                <p>• Тестировщик <span class="status">offline</span></p>
            </div>
            
            <div class="card">
                <h3>📋 Задачи</h3>
                <p>• Развертывание системы <span class="status">completed</span></p>
                <p>• Интеграция Telegram <span class="status">in progress</span></p>
                <p>• Оптимизация API <span class="status">pending</span></p>
            </div>
            
            <div class="card">
                <h3>📁 Документы</h3>
                <p>• Техническая документация (PDF, 2.5MB)</p>
                <p>• API руководство (MD, 1.2MB)</p>
                <p>• Установка и настройка (DOC, 3.1MB)</p>
            </div>
            
            <div class="card">
                <h3>🌐 API Статус</h3>
                <p><span class="status">Online</span> - система работает</p>
                <p>Версия: 2025.1.0</p>
                <div>
                    <a href="/health" class="btn">Статус API</a>
                    <a href="/api" class="btn">Информация</a>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Обновляем порт в реальном времени
        fetch('/health')
            .then(r => r.json())
            .then(data => {
                document.getElementById('port').textContent = data.port;
            });
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
        "port": port,
        "message": "Система работает идеально!"
    })

@app.get("/api")
async def api_info():
    return JSONResponse({
        "endpoints": {
            "/": "Главная страница",
            "/health": "Статус системы", 
            "/api": "Информация API",
            "/users": "Список пользователей",
            "/tasks": "Список задач"
        },
        "status": "active",
        "port": port
    })

@app.get("/users")
async def get_users():
    return JSONResponse([
        {"id": 1, "name": "Администратор", "status": "online"},
        {"id": 2, "name": "Разработчик", "status": "online"},
        {"id": 3, "name": "Тестировщик", "status": "offline"}
    ])

@app.get("/tasks") 
async def get_tasks():
    return JSONResponse([
        {"id": 1, "title": "Развертывание системы", "status": "completed"},
        {"id": 2, "title": "Интеграция Telegram", "status": "in_progress"},
        {"id": 3, "title": "Оптимизация API", "status": "pending"}
    ])

def find_free_port():
    """Находит свободный порт"""
    for port in [8080, 3000, 5000, 8000, 9000]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except:
            continue
    return 8080  # fallback

port = find_free_port()

if __name__ == "__main__":
    print(f"🚀 Запускаем рабочий сервер на порту {port}...")
    print(f"🌐 Откройте: http://localhost:{port}")
    print(f"📊 Статус: http://localhost:{port}/health")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
