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
