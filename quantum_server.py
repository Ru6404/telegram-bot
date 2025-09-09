from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import time

app = FastAPI()

# Добавляем все endpoints
@app.get("/")
async def root():
    return {"message": "Quantum System 2025 работает!", "status": "online"}

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "version": "2025.1.0",
        "timestamp": time.time(),
        "server": "Quantum System"
    }

@app.get("/api")
async def api_info():
    return {
        "endpoints": {
            "/": "Главная страница",
            "/health": "Статус системы",
            "/api": "Информация API",
            "/users": "Список пользователей",
            "/tasks": "Список задач"
        }
    }

@app.get("/users")
async def get_users():
    return [
        {"id": 1, "name": "Администратор", "role": "admin", "status": "online"},
        {"id": 2, "name": "Разработчик", "role": "developer", "status": "online"},
        {"id": 3, "name": "Тестировщик", "role": "tester", "status": "offline"}
    ]

@app.get("/tasks")
async def get_tasks():
    return [
        {"id": 1, "title": "Развертывание системы", "status": "completed", "priority": "high"},
        {"id": 2, "title": "Интеграция Telegram", "status": "in_progress", "priority": "medium"},
        {"id": 3, "title": "Оптимизация API", "status": "pending", "priority": "low"}
    ]

if __name__ == "__main__":
    print("🚀 Запускаем Quantum Server с всеми endpoints...")
    print("🌐 Главная: http://127.0.0.1:8080")
    print("📊 Статус: http://127.0.0.1:8080/health")
    print("👥 Пользователи: http://127.0.0.1:8080/users")
    print("📋 Задачи: http://127.0.0.1:8080/tasks")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
