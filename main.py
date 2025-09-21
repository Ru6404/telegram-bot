from fastapi import FastAPI

app = FastAPI()

# Тестовый эндпоинт
@app.get("/")
def root():
    return {"message": "API работает ✅"}

# Эндпоинт: список клиентов
@app.get("/api/clients")
def get_clients():
    return [
        {"id": 1, "name": "Иван"},
        {"id": 2, "name": "Мария"}
    ]

# Эндпоинт: список заявок
@app.get("/api/orders")
def get_orders():
    return [
        {"id": 101, "status": "новая"},
        {"id": 102, "status": "в работе"}
    ]
