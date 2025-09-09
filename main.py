from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
from datetime import datetime
from passlib.context import CryptContext

app = FastAPI(title="Auto-Cloud API", version="1.0")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = []
todos_db = []

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""

def get_password_hash(password):
    return pwd_context.hash(password)

@app.on_event("startup")
async def startup():
    predefined_users = [
        {"id": "9b1e94b9-3565-4148-903f-3949d9080764", "username": "ruslan6404", "email": "ruslan6404kim@gmail.com", "password": get_password_hash("auto-pass-123")},
        {"id": "0e049ea1-6a4c-46da-8f59-8f28e72e26bf", "username": "r91815984", "email": "r91815984@gmail.com", "password": get_password_hash("auto-pass-456")}
    ]
    
    for user in predefined_users:
        users_db.append(user)
    
    test_todos = [
        {"title": "Изучить FastAPI", "description": "Освоить основы"},
        {"title": "Настроить облако", "description": "Развернуть сервер"},
        {"title": "Создать бота", "description": "Интегрировать с Telegram"}
    ]
    
    for todo in test_todos:
        todos_db.append({
            "id": str(uuid.uuid4()),
            "title": todo["title"],
            "description": todo["description"],
            "completed": False,
            "user_id": users_db[0]["id"],
            "created_at": datetime.utcnow().isoformat()
        })
    print("🚀 Auto-Cloud API запущен!")

@app.get("/")
async def root():
    return {"message": "🚀 Auto-Cloud API в облаке!", "users": len(users_db), "todos": len(todos_db)}

@app.get("/users")
async def get_users():
    return users_db

@app.get("/todos")
async def get_todos():
    return todos_db

@app.post("/register")
async def register(user: UserCreate):
    user_id = str(uuid.uuid4())
    new_user = {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "password": get_password_hash(user.password)
    }
    users_db.append(new_user)
    return new_user

@app.post("/todos")
async def create_todo(todo: TodoCreate):
    todo_id = str(uuid.uuid4())
    new_todo = {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "user_id": users_db[0]["id"] if users_db else "unknown"
    }
    todos_db.append(new_todo)
    return new_todo
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Создаем директорию для шаблонов
os.makedirs("templates", exist_ok=True)

@app.get("/web", response_class=HTMLResponse)
async def web_page():
    """Веб-страница для браузера"""
    return """
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
        
        <h2>🔗 Доступные endpoints:</h2>
        <div class="endpoint"><strong>GET /</strong> - Главная страница</div>
        <div class="endpoint"><strong>GET /health</strong> - Проверка здоровья</div>
        <div class="endpoint"><strong>GET /users</strong> - Пользователи (2)</div>
        <div class="endpoint"><strong>GET /todos</strong> - Задачи (3)</div>
        <div class="endpoint"><strong>GET /web</strong> - Эта страница</div>

        <script>
            fetch('/')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('stats').innerHTML = 
                        '👥 Пользователей: ' + data.users + '<br>' +
                        '✅ Задач: ' + data.todos + '<br>' +
                        '📝 ' + data.message;
                });
        </script>
    </body>
    </html>
    """
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
