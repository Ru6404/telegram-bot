from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем CORS (для работы с любым браузером/телеграмом)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пример данных
clients = [{"id":1,"name":"Иван"},{"id":2,"name":"Мария"}]
requests_db = [{"id":1,"title":"Заявка 1"},{"id":2,"title":"Заявка 2"}]

# API маршруты
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

# HTML-интерфейс CRM
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CRM Панель</title>
        <style>
            body {font-family: Arial; padding: 20px;}
            button {margin:5px; padding:10px; font-size:16px; cursor:pointer;}
            table {border-collapse: collapse; margin-top:10px;}
            th, td {border:1px solid black; padding:5px;}
            .accepted {color:green; font-weight:bold;}
            .rejected {color:red; font-weight:bold;}
        </style>
    </head>
    <body>
        <h2>CRM Панель</h2>
        <button onclick="loadClients()">📋 Клиенты</button>
        <button onclick="loadRequests()">📝 Заявки</button>
        <button onclick="loadStats()">📊 Статистика</button>

        <div id="output"></div>

        <script>
            async function loadClients(){
                const res = await fetch('/api/clients');
                const data = await res.json();
                let html = '<h3>Клиенты</h3><table><tr><th>ID</th><th>Имя</th></tr>';
                data.forEach(c=>{html += `<tr><td>${c.id}</td><td>${c.name}</td></tr>`});
                html += '</table>';
                document.getElementById('output').innerHTML = html;
            }

            async function loadRequests(){
                const res = await fetch('/api/requests');
                const data = await res.json();
                let html = '<h3>Заявки</h3><table><tr><th>ID</th><th>Название</th><th>Статус</th><th>Действие</th></tr>';
                data.forEach(r=>{
                    html += `<tr>
                                <td>${r.id}</td>
                                <td>${r.title}</td>
                                <td class="${r.status||''}">${r.status||''}</td>
                                <td>
                                    <button onclick="actionRequest(${r.id}, 'accepted')">✅ Принять</button>
                                    <button onclick="actionRequest(${r.id}, 'rejected')">❌ Отказать</button>
                                </td>
                             </tr>`;
                });
                html += '</table>';
                document.getElementById('output').innerHTML = html;
            }

            async function loadStats(){
                const res = await fetch('/api/stats');
                const data = await res.json();
                let html = '<h3>Статистика</h3><ul>';
                for(let k in data){
                    html += `<li>${k}: ${data[k]}</li>`;
                }
                html += '</ul>';
                document.getElementById('output').innerHTML = html;
            }

            async function actionRequest(id, action){
                await fetch(`/api/request/${id}/action?action=${action}`, {method:'POST'});
                loadRequests(); // обновляем таблицу после действия
            }
        </script>
    </body>
    </html>
    """

