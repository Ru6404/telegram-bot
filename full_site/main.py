from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Разрешаем доступ с любых устройств
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Пример данных
clients = [{"id": 1, "name": "Иван"}, {"id": 2, "name": "Мария"}]
requests_db = [{"id": 1, "title": "Заявка 1"}, {"id": 2, "title": "Заявка 2"}]

# HTML интерфейс с красивыми кнопками
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>CRM Панель</h2>
    <button onclick="fetch('/api/clients').then(r=>r.json()).then(d=>alert(JSON.stringify(d)))">📋 Клиенты</button>
    <button onclick="fetch('/api/requests').then(r=>r.json()).then(d=>alert(JSON.stringify(d)))">📝 Заявки</button>
    <button onclick="fetch('/api/stats').then(r=>r.json()).then(d=>alert(JSON.stringify(d)))">📊 Статистика</button>
    <button onclick="alert('Помощь ❓')">❓ Помощь</button>
    """

# API
@app.get("/api/clients")
def get_clients():
    return clients

@app.get("/api/requests")
def get_requests():
    return requests_db

@app.post("/api/request/{req_id}/action")
def request_action(req_id: int, action: str):
    for r in requests_db:
        if r["id"] == req_id:
            r["status"] = action
            return {"result": "ok", "id": req_id, "status": action}
    return {"error": "not found"}

@app.get("/api/stats")
def get_stats():
    return {"clients": len(clients), "requests": len(requests_db)}
