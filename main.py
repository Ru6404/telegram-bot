from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
from datetime import datetime
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

app = FastAPI(title="Auto-Cloud API")

# Модели данных
class UserCreate(BaseModel):
    username: str
    email: str

class TodoCreate(BaseModel):
    title: str
    description: str

# Базы данных в памяти
users_db = []
todos_db = []

# API endpoints
@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Auto-Cloud API!"}

@app.get("/users")
async def get_users():
    return users_db

@app.post("/users")
async def create_user(user: UserCreate):
    user_data = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email,
        "created_at": datetime.now().isoformat()
    }
    users_db.append(user_data)
    return user_data

@app.get("/todos")
async def get_todos():
    return todos_db

@app.post("/todos")
async def create_todo(todo: TodoCreate):
    todo_data = {
        "id": str(uuid.uuid4()),
        "title": todo.title,
        "description": todo.description,
        "created_at": datetime.now().isoformat()
    }
    todos_db.append(todo_data)
    return todo_data

# Единый стиль для всех страниц
COMMON_STYLE = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
        color: #333;
    }
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .header {
        text-align: center;
        margin-bottom: 40px;
        color: white;
    }
    .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .header p {
        font-size: 1.2em;
        opacity: 0.9;
    }
    .nav {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
        flex-wrap: wrap;
    }
    .nav a {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 12px 25px;
        text-decoration: none;
        border-radius: 25px;
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.3);
    }
    .nav a:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    .card {
        background: rgba(255,255,255,0.95);
        padding: 25px;
        margin: 20px 0;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    .card h3 {
        color: #667eea;
        margin-bottom: 15px;
        font-size: 1.4em;
    }
    .card p {
        margin: 8px 0;
        line-height: 1.6;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 25px;
        margin-top: 30px;
    }
    .empty-state {
        text-align: center;
        padding: 40px;
        background: rgba(255,255,255,0.2);
        border-radius: 15px;
        color: white;
    }
    .api-link {
        display: inline-block;
        margin-top: 20px;
        color: #667eea;
        background: white;
        padding: 8px 15px;
        border-radius: 20px;
        text-decoration: none;
        font-weight: bold;
    }
</style>
"""

# HTML страницы
@app.get("/", response_class=HTMLResponse)
async def home_page():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auto-Cloud - Главная</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Auto-Cloud API</h1>
                <p>Автоматизированное облачное решение для управления пользователями и задачами</p>
            </div>
            
            <div class="nav">
                <a href="/users-page">👥 Пользователи</a>
                <a href="/todos-page">✅ Задачи</a>
                <a href="/users">📊 API Users</a>
                <a href="/todos">⚙️ API Todos</a>
            </div>

            <div class="card">
                <h3>🎯 О системе</h3>
                <p>Auto-Cloud предоставляет современный API для управления пользователями и задачами с красивым веб-интерфейсом.</p>
                <p>📈 <strong>Пользователей в системе:</strong> {len(users_db)}</p>
                <p>✅ <strong>Задач в системе:</strong> {len(todos_db)}</p>
                
                <a href="/users-page" class="api-link">Перейти к интерфейсу →</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/users-page", response_class=HTMLResponse)
async def users_page():
    users_html = "".join([
        f"""
        <div class="card">
            <h3>👤 {user.get('username', 'No name')}</h3>
            <p>📧 <strong>Email:</strong> {user.get('email', 'No email')}</p>
            <p>🆔 <strong>ID:</strong> {user.get('id', 'No ID')}</p>
            <p>📅 <strong>Создан:</strong> {user.get('created_at', '')[:10]}</p>
        </div>
        """ for user in users_db
    ])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Пользователи - Auto-Cloud</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>👥 Пользователи системы</h1>
                <p>Управление пользователями Auto-Cloud</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 Главная</a>
                <a href="/todos-page">✅ Задачи</a>
                <a href="/users">📊 API</a>
            </div>

            <div class="grid">
                {users_html if users_db else '<div class="empty-state"><h3>😔 Нет пользователей</h3><p>Добавьте первого пользователя через API</p></div>'}
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/todos-page", response_class=HTMLResponse)
async def todos_page():
    todos_html = "".join([
        f"""
        <div class="card">
            <h3>✅ {todo.get('title', 'No title')}</h3>
            <p>{todo.get('description', 'No description')}</p>
            <p>📅 <strong>Создана:</strong> {todo.get('created_at', '')[:10]}</p>
            <p>🆔 <strong>ID:</strong> {todo.get('id', 'No ID')}</p>
        </div>
        """ for todo in todos_db
    ])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Задачи - Auto-Cloud</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Задачи системы</h1>
                <p>Управление задачами Auto-Cloud</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 Главная</a>
                <a href="/users-page">👥 Пользователи</a>
                <a href="/todos">⚙️ API</a>
            </div>

            <div class="grid">
                {todos_html if todos_db else '<div class="empty-state"><h3>✅ Нет задач</h3><p>Добавьте первую задачу через API</p></div>'}
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
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
