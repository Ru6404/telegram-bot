from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class InstantAIHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """Устанавливает CORS заголовки"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        """Обрабатывает preflight запросы"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Для проверки работы сервера"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write('🚀 AI Server is running! Use POST /api/ai/ask'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Обрабатывает AI запросы"""
        if self.path == '/api/ai/ask':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                question = data.get('question', '').lower().strip()
                print(f"📨 Вопрос: '{question}'")
                
                response = self.generate_response(question)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self._set_cors_headers()
                self.end_headers()
                
                response_data = json.dumps({
                    "answer": response,
                    "success": True
                })
                self.wfile.write(response_data.encode('utf-8'))
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self._set_cors_headers()
                self.end_headers()
                error_data = json.dumps({
                    "success": False,
                    "error": str(e),
                    "answer": "⚠️ Ошибка сервера"
                })
                self.wfile.write(error_data.encode('utf-8'))
    
    def generate_response(self, question):
        """Генерирует умные ответы"""
        current_date = datetime.now().strftime('%d.%m.%Y')
        
        if 'привет' in question:
            return "👋 Привет! Я ИИ-помощник с новостями Узбекистана!"
        
        if 'новости' in question and 'узбек' in question:
            if 'сегодня' in question:
                return f"""📰 НОВОСТИ УЗБЕКИСТАНА ({current_date}):

• Центробанк сохранил ставку 14%
• Новые инвестиции в IT: $500 млн
• Рекорд туризма: 1.2 млн visitors
• Сборная готовится к чемпионату Азии

💡 Что интересует: экономика, спорт, технологии?"""
            else:
                return """📰 Новости Узбекистана:

• Экономический рост: 5.8% в 2024
• ВВП на душу: $2,500
• Инфляция: 10.2% за год
• Инвестиции: $7.8 млрд

📅 Уточните: "новости сегодня\""""
        
        if 'что ты можешь' in question:
            return """🤖 Я МОГУ:
• 📰 Новости Узбекистана
• 🧮 Решение примеров  
• ⏰ Время и дату
• 💡 Ответы на вопросы

🎯 Примеры: "Новости сегодня", "15*20", "Который час\""""
        
        if any(op in question for op in ['+', '-', '*', '/', 'сколько будет']):
            try:
                expr = question.replace('сколько будет', '').strip()
                expr = expr.replace('×', '*').replace('÷', '/')
                if all(c in '0123456789+-*/. ()' for c in expr):
                    result = eval(expr)
                    return f"🧮 {expr} = {result}"
            except:
                return "❌ Не могу вычислить"
        
        if any(word in question for word in ['время', 'который час', 'дата']):
            return f"⏰ {datetime.now().strftime('%H:%M, %d.%m.%Y')}"
        
        return "🤔 Интересный вопрос! Уточните детали."

if __name__ == '__main__':
    server_address = ('127.0.0.1', 5050)
    httpd = HTTPServer(server_address, InstantAIHandler)
    print("🚀 ИИ-сервер запущен на http://127.0.0.1:5050")
    print("✅ Готов к работе!")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
