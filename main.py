from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

clients = [{"id":1,"name":"Иван"},{"id":2,"name":"Мария"}]

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/api/clients")
def get_clients():
    return JSONResponse(content=clients)
