from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import socket
import time
from typing import Dict, List
import json

app = FastAPI(title="Quantum Universal System 2025")

# Моковые данные
USERS = [
    {"id": 1, "name": "Администратор", "role": "admin", "status": "online"},
    {"id": 2, "name": "Разработчик", "role": "developer", "status": "online"},
    {"id": 3, "name": "Тестировщик", "role": "tester", "status": "offline"}
]

TASKS = [
    {"id": 1, "title": "Развертывание системы", "status": "completed", "priority": "high"},
    {"id": 2, "title": "Интеграция Telegram", "status": "in_progress", "priority": "medium"},
    {"id": 3, "title": "Оптимизация API", "status": "pending", "priority": "low"}
]

DOCUMENTS = [
    {"id": 1, "title": "Техническая документация", "type": "pdf", "size": "2.5MB"},
    {"id": 2, "title": "API руководство", "type": "md", "size": "1.2MB"},
    {"id": 3, "title": "Установка и настройка", "type": "doc", "size": "3.1MB"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Universal System 2025 🚀</title>
    <style>
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #4ade80;
            --warning: #fbbf24;
            --danger: #ff4757;
            --dark: #1f2937;
            --light: #f8fafc;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            min-height: 100vh; color: white; line-height: 1.6;
        }
        
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        .header { 
            text-align: center; 
            margin-bottom: 3rem; 
            padding: 2rem; 
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        .logo { font-size: 4rem; margin-bottom: 1rem; animation: pulse 2s infinite; }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .title { font-size: 2.5rem; font-weight: 300; margin-bottom: 0.5rem; }
        .subtitle { font-size: 1.1rem; opacity: 0.9; margin-bottom: 1rem; }
        .port-info { 
            background: rgba(255, 255, 255, 0.2); 
            padding: 0.5rem 1rem; 
            border-radius: 20px; 
            display: inline-block; 
            font-size: 0.9rem;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }
        
        .section {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .section-title {
            font-size: 1.3rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .item {
            padding: 0.8rem;
            margin: 0.5rem 0;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            border-left: 4px solid var(--success);
        }
        
        .item-offline { border-left-color: var(--danger); }
        .item-warning { border-left-color: var(--warning); }
        
        .status {
            display: inline-block;
            padding: 0.2rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .status-online { background: var(--success); color: white; }
        .status-offline { background: var(--danger); color: white; }
        .status-progress { background: var(--warning); color: black; }
        
        .api-section {
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
        }
        
        .btn {
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: rgba(255, 255, 255, 0.2);
            border: none;
            border-radius: 25px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
            margin: 0.3rem;
        }
        
        .btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        @media (max-width: 768px) {
            .dashboard { grid-template-columns: 1fr; }
            .title { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡</div>
            <h1 class="title">Quantum Universal System 2025</h1>
            <p class="subtitle">Полная автоматизация и управление</p>
            <div class="port-info">Порт: {{PORT}}</div>
        </div>
        
        <div class="dashboard">
            <!-- Пользователи -->
            <div class="section">
                <h2 class="section-title">👥 Пользователи</h2>
                {{USERS}}
            </div>
            
            <!-- Задачи -->
            <div class="section">
                <h2 class="section-title">📋 Задачи</h2>
                {{TASKS}}
            </div>
            
            <!-- Документы -->
            <div class="section">
                <h2 class="section-title">📁 Документы</h2>
                {{DOCUMENTS}}
            </div>
            
            <!-- Статус API -->
            <div class="section">
                <h2 class="section-title">🌐 Статус API</h2>
                <div class="api-section">
                    <strong>Endpoint:</strong> /health<br>
                    <strong>Метод:</strong> GET<br>
                    <strong>Статус:</strong> <span class="status status-online">Online</span><br>
                    <strong>Версия:</strong> 2025.1.0
                </div>
                
                <div class="api-section">
                    <strong>Endpoint:</strong> /api<br>
                    <strong>Метод:</strong> GET<br>
                    <strong>Описание:</strong> Информация о API<br>
                    <strong>Доступ:</strong> <span class="status status-online">Public</span>
                </div>
                
                <a href="/health" class="btn">📊 Проверить статус</a>
                <a href="/api" class="btn">🔧 API информация</a>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 Quantum Universal System | Автопорт: {{PORT}}</p>
            <p>Все системы работают стабильно 🚀</p>
        </div>
    </div>
    
    <script>
        // Автообновление каждые 30 секунд
        setInterval(() => {
            fetch('/health')
                .then(response => response.json())
                .then(data => {
                    console.log('Система онлайн:', data.status);
                })
                .catch(error => {
                    console.error('Ошибка подключения:', error);
                });
        }, 30000);
    </script>
</body>
</html>
"""

def render_html(port: int):
    """Генерация HTML с данными"""
    users_html = "\n".join([
        f'<div class="item {"" if user["status"] == "online" else "item-offline"}">'
        f'<strong>{user["name"]}</strong> '
        f'<span class="status status-{user["status"]}">{user["status"]}</span><br>'
        f'<small>Роль: {user["role"]}</small>'
        f'</div>'
        for user in USERS
    ])
    
    tasks_html = "\n".join([
        f'<div class="item {"" if task["status"] == "completed" else "item-warning"}">'
        f'<strong>{task["title"]}</strong> '
        f'<span class="status status-{"online" if task["status"] == "completed" else "progress"}">{task["status"]}</span><br>'
        f'<small>Приоритет: {task["priority"]}</small>'
        f'</div>'
        for task in TASKS
    ])
    
    docs_html = "\n".join([
        f'<div class="item">'
        f'<strong>{doc["title"]}</strong><br>'
        f'<small>Тип: {doc["type"]} | Размер: {doc["size"]}</small>'
        f'</div>'
        for doc in DOCUMENTS
    ])
    
    return HTML_TEMPLATE \
        .replace("{{PORT}}", str(port)) \
        .replace("{{USERS}}", users_html) \
        .replace("{{TASKS}}", tasks_html) \
        .replace("{{DOCUMENTS}}", docs_html)

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(render_html(port))

@app.get("/health")
async def health():
    return JSONResponse({
        "status": "healthy",
        "version": "2025.1.0",
        "timestamp": time.time(),
        "server": "Quantum Universal System",
        "port": port,
        "users_online": sum(1 for u in USERS if u["status"] == "online"),
        "tasks_total": len(TASKS)
    })

@app.get("/api")
async def api_info():
    return JSONResponse({
        "endpoints": {
            "/": "Главная страница с интерфейсом",
            "/health": "Статус системы и метрики",
            "/api": "Информация о API",
            "/users": "Список пользователей",
            "/tasks": "Список задач",
            "/documents": "Список документов"
        },
        "system_info": {
            "port": port,
            "start_time": time.time(),
            "version": "2025.1.0"
        }
    })

@app.get("/users")
async def get_users():
    return JSONResponse(USERS)

@app.get("/tasks")
async def get_tasks():
    return JSONResponse(TASKS)

@app.get("/documents")
async def get_documents():
    return JSONResponse(DOCUMENTS)

def find_free_port():
    """Находит свободный порт автоматически"""
    ports = [8080, 3000, 5000, 8000, 9000, 8081, 8082, 8083]
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    # Если все заняты, берем случайный
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# Автоматический выбор порта
port = find_free_port()

if __name__ == "__main__":
    print(f"🚀 Запускаем Universal System на порту {port}...")
    print(f"🌐 Главная: http://localhost:{port}")
    print(f"📊 Статус: http://localhost:{port}/health")
    print(f"🔧 API: http://localhost:{port}/api")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
