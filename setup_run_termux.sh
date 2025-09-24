#!/bin/bash

# ==== НАСТРОЙКИ ====
APP_PASSWORD="<вставь_сюда_твой_App_Password>"
EMAIL_FROM="ruslan6404kim@gmail.com"
EMAIL_TO="r91815984@gmail.com"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
MODEL_NAME="llama2"
PORT=8000
# ====================

echo "🔄 Обновляем Termux..."
pkg update -y && pkg upgrade -y

echo "🐍 Проверяем Python..."
pkg install python -y

echo "📦 Устанавливаем pip и зависимости..."
python3 -m ensurepip
python3 -m pip install --upgrade pip
pip3 install fastapi uvicorn python-dotenv requests

echo "🛠 Проверяем Ollama..."
if ! command -v ollama &> /dev/null
then
    echo "📥 Устанавливаем Ollama..."
    pkg install ollama -y
else
    echo "✅ Ollama уже установлен"
fi

echo "📥 Скачиваем модель $MODEL_NAME..."
ollama pull $MODEL_NAME

# Создаём .env полностью автоматически
cat <<EOL > .env
EMAIL_FROM=$EMAIL_FROM
EMAIL_TO=$EMAIL_TO
SMTP_SERVER=$SMTP_SERVER
SMTP_PORT=$SMTP_PORT
SMTP_USER=$EMAIL_FROM
SMTP_PASS=$APP_PASSWORD
MODEL_NAME=$MODEL_NAME
PORT=$PORT
EOL

# Создаём server.py если не существует
cat <<'EOL' > server.py
import os
import subprocess
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
PORT = int(os.getenv("PORT", 8000))
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

logging.basicConfig(filename="app.log", level=logging.INFO)

def send_error_email(error_text: str):
    try:
        msg = MIMEText(f"❌ Ошибка сервера:\n\n{error_text}")
        msg["Subject"] = "Ошибка LLM сервера"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        logging.info("✅ Ошибка отправлена на Email")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке Email: {repr(e)}")

app = FastAPI()

class Query(BaseModel):
    prompt: str

@app.post("/ask")
def ask_model(query: Query):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, "--prompt", query.prompt],
            capture_output=True, text=True, check=True
        )
        answer = result.stdout.strip()
        logging.info(f"Запрос: {query.prompt} | Ответ: {answer}")
        return {"answer": answer}
    except subprocess.CalledProcessError as e:
        error_text = e.stderr
        logging.error(f"Ошибка Ollama: {error_text}")
        send_error_email(error_text)
        raise HTTPException(status_code=500, detail="Ошибка модели")
EOL

echo "🚀 Запускаем сервер на порту $PORT..."
uvicorn server:app --reload --host 0.0.0.0 --port $PORT
