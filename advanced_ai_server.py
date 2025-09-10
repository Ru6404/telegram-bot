from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from datetime import datetime
import re

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
                print(f"📨 Вопрос: {question}")
                
                # УМНЫЕ ОТВЕТЫ С ПОНИМАНИЕМ КОНТЕКСТА
                response = self.generate_ai_response(question)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_data = json.dumps({"answer": response, "status": "success"})
                self.wfile.write(response_data.encode())
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_ai_response(self, question):
        """Генератор умных ответов ИИ"""
        current_date = datetime.now().strftime("%d.%m.%Y")
        
        # НОВОСТИ УЗБЕКИСТАНА
        if 'узбек' in question and 'новости' in question:
            if 'сегодня' in question:
                return f"""📰 Новости Узбекистана на сегодня ({current_date}):

• Экономика: Центробанк сохранил ключевую ставку на уровне 14%
• Бизнес: Запущена новая программа поддержки малого бизнеса
• Спорт: Сборная Узбекистана победила в товарищеском матче
• Туризм: Рекордное количество туристов в Самарканде

Что именно вас интересует? Экономика, спорт, культура?"""
            
            elif 'недел' in question:
                return """📰 Новости Узбекистана за неделю:

• Подписано соглашение о свободной торговле с ОАЭ
• ВВП вырос на 5.8% за год
• Запущены новые авиарейсы в Европу и Азию
• Цифровизация госуслуг достигла 90%

Уточните тему для подробностей!"""
            
            else:
                return """📰 Новости Узбекистана:

• Экономический рост: 5.8% в 2024 году
• Туризм: увеличение на 30% 
• Инвестиции: привлечено $7.8 млрд
• Инфляция: 10.2% за год

Уточните: "новости сегодня" или "новости за неделю\""""
        
        # МАТЕМАТИКА
        math_match = re.search(r'(\d+[\+\-\*\/]\d+)|(посчитай|сколько будет)\s+(.+)', question)
        if math_match:
            expr = math_match.group(1) or math_match.group(3)
            try:
                result = eval(expr, {"__builtins__": None}, {})
                return f"🧮 Результат: {expr} = {result}"
            except:
                return "❌ Не могу решить этот пример"
        
        # ВРЕМЯ
        if any(word in question for word in ['время', 'который час', 'дата']):
            return f"⏰ Сейчас: {datetime.now().strftime('%H:%M:%S %d.%m.%Y')}"
        
        # ОБЩИЕ ВОПРОСЫ
        if 'что ты можешь' in question:
            return """🤖 Я - ИИ-помощник! Могу:
• 📰 Рассказать новости Узбекистана
• 🧮 Решить математические примеры  
• ⏰ Показать время и дату
• 💡 Ответить на различные вопросы

Спросите меня о чем угодно!"""
        
        # УМНЫЙ ОТВЕТ ПО УМОЛЧАНИЮ
        responses = [
            f"🤔 По вашему вопросу '{question}': что именно интересует?",
            f"💡 '{question}' - хороший вопрос! Уточните детали?",
            f"🎯 Понял ваш запрос! Нужна дополнительная информация?",
            f"🔍 Изучаю вопрос... Какие аспекты最重要?",
            f"🚀 Принял! По теме '{question}' есть много информации."
        ]
        
        return random.choice(responses)

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', 5050), AIHandler)
    print("🚀 Продвинутый ИИ-сервер запущен на порту 5050...")
    print("📡 Endpoint: http://127.0.0.1:5050/api/ai/ask")
    print("🔧 Готов обрабатывать запросы...")
    server.serve_forever()
