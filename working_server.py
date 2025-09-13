from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()

# Кастомный JSONResponse с правильной кодировкой UTF-8
class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

    def render(self, content) -> bytes:
        return json.dumps(
            jsonable_encoder(content),
            ensure_ascii=False,  # Важно! для русского текста
            indent=2
        ).encode("utf-8")

@app.get("/", response_class=UTF8JSONResponse)
async def root():
    return {
        "message": "✅ Auto-Cloud API работает отлично!",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "test": "/test"
        }
    }

@app.get("/health", response_class=UTF8JSONResponse)
async def health_check():
    return {
        "status": "healthy",
        "service": "auto-cloud-api",
        "message": "Сервер работает нормально"
    }

@app.get("/status", response_class=UTF8JSONResponse)
async def status_check():
    return {
        "status": "online",
        "message": "Все системы в порядке"
    }

@app.get("/test", response_class=UTF8JSONResponse)
async def test_endpoint():
    return {
        "test": "success",
        "message": "Тест пройден успешно!",
        "data": {
            "пользователи": 5,
            "задачи": 12,
            "проекты": 3
        }
    }
