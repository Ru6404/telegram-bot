from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from datetime import datetime

class AIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/ai/ask':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                question = data.get('question', '').lower()
                print(f"📨 Получен вопрос: {question}")
                
                # Умные ответы
                if 'узбек' in question:
                    if 'новости' in question:
                        response = "🇺🇿 Новости Узбекистана: Экономика растет на 5.8%, туризм увеличился на 30%. Запущена новая программа поддержки бизнеса!"
                    elif 'изменения' in question:
                        response = "🔍 Изменения в Узбекистане: Цифровизация госуслуг, налоговые реформы, развитие зеленой энергетики"
                    else:
                        response = "🇺🇿 Узбекистан - прекрасная страна с богатой культурой и быстро развивающейся экономикой!"
                
                elif 'что ты можешь' in question:
                    response = "🤖 Я могу отвечать на вопросы, помогать с информацией о Узбекистане, решать примеры и многое другое!"
                
                elif 'привет' in question:
                    response = "👋 Привет! Я ваш ИИ-помощник. Задайте мне любой вопрос!"
                
                else:
                    response = "🤔 Интересный вопрос! Уточните детали для более точного ответа."
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_data = json.dumps({"answer": response})
                self.wfile.write(response_data.encode())
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 5050), AIHandler)
    print("🚀 Простой ИИ-сервер запущен на порту 5050...")
    print("📡 Доступен по: http://127.0.0.1:5050/api/ai/ask")
    server.serve_forever()
