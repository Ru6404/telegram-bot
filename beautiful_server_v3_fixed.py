from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Auto-Cloud API",
    description="Приватное FastAPI приложение для управления задачами",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Простое подключение к SQLite
def get_db_connection():
    try:
        conn = sqlite3.connect('test.db')
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return None

@app.get("/")
async def root():
    return {
        "message": "Auto-Cloud API работает!",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "status": "/status"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auto-cloud-api"}

@app.get("/status")
async def system_status():
    try:
        conn = get_db_connection()
        if conn:
            # Проверяем наличие таблиц
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            return {
                "status": "online",
                "database": "connected",
                "tables": [table['name'] for table in tables] if tables else []
            }
        else:
            return {"status": "online", "database": "disconnected"}
    except Exception as e:
        return {"status": "online", "database": "error", "error": str(e)}

# Простые тестовые endpoints
@app.get("/api/test")
async def test_endpoint():
    return {"message": "Test successful", "code": 200}

@app.get("/api/users")
async def get_users():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users LIMIT 5")
            users = cursor.fetchall()
            conn.close()
            return {"users": [dict(user) for user in users] if users else []}
        return {"users": []}
    except:
        return {"users": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
