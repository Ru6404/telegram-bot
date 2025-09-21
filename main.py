from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

clients = [{"id": 1, "name": "Иван"}, {"id": 2, "name": "Мария"}]
requests_db = [
    {"id": 1, "title": "Заявка 1", "status": "new"},
    {"id": 2, "title": "Заявка 2", "status": "new"}
]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "clients": clients, "requests": requests_db})

@app.get("/api/clients")
async def get_clients():
    return clients

@app.get("/api/requests")
async def get_requests():
    return requests_db

@app.get("/api/stats")
async def get_stats():
    total = len(requests_db)
    accepted = sum(1 for r in requests_db if r["status"] == "accepted")
    rejected = sum(1 for r in requests_db if r["status"] == "rejected")
    return {"total": total, "accepted": accepted, "rejected": rejected}

@app.post("/api/request/{req_id}/action")
async def action_request(req_id: int, action: str = Form(...)):
    for r in requests_db:
        if r["id"] == req_id:
            if action in ["accepted", "rejected"]:
                r["status"] = action
                return {"success": True, "request": r}
    return {"success": False, "error": "Request not found"}
