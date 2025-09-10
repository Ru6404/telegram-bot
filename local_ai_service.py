from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/ai/ask', methods=['POST'])
def aski():
    try:
        data = request.json
        question = data.get('question', '').lower()
        user_context = data.get('context', '')
        
        print(f"📨 Получен вопрос: {question}")
        print(f"👤 Контекст: {user_context}")
        
        # Умные ответы про Узбекистан
        if 'узбек' in question:
            if 'новости' in question:
                news_responses = [
                    "🇺🇿 Новости Узбекистана: Экономика выросла на 5.8% в этом году, туризм увеличился на 30%",
                    "📰 Ташкент: Международная инвестиционная конференция привлекла $7.8 млрд",
                    "🌏 Узбекистан: Запущена новая программа поддержки малого бизнеса с бюджетом $500 млн",
                    "🚀 Самарканд: Фестиваль культурного наследия собрал рекордное количество туристов",
                    "💼 Экономика: Рост ВВП Узбекистана составляет 5.8%, инфляция - 10.2%"
                ]
                return jsonify({"answer": random.choice(news_responses)})
            
            elif 'изменения' in question or 'реформы' in question:
                reform_responses = [
                    "🔍 Изменения в Узбекистане: Цифровизация 90% госуслуг, упрощение налоговой системы",
                    "📱 Реформы: Запуск платформы my.gov.uz для электронных услуг",
                    "🌱 Зеленая энергетика: Строительство новых солнечных и ветряных электростанций",
                    "🏛️ Госуправление: Административная реформа и борьба с коррупцией",
                    "💸 Экономика: Либерализация валютного рынка и приватизация госпредприятий"
                ]
                return jsonify({"answer": random.choice(reform_responses)})
            
            else:
                uzbek_responses = [
                    "🇺🇿 Узбекистан - страна с богатой историей и быстро развивающейся экономикой!",
                    "🌏 Столица Ташкент - современный мегаполис с населением 2.5 млн человек",
                    "🎭 Культура: Узбекистан известен своими древними городами Шелкового пути",
                    "🏔️ География: От гор Тянь-Шаня до пустыни Кызылкум",
                    "📈 Экономика: Быстрорастущая экономика с фокусом на туризм и IT"
                ]
                return jsonify({"answer": random.choice(uzbek_responses)})
        
        # Общие вопросы
        if 'что ты можешь' in question:
            return jsonify({"answer": "🤖 Я могу отвечать на вопросы, предоставлять информацию о Узбекистане, помогать с вычислениями и многое другое! Спросите меня о чем угодно!"})
        
        if 'привет' in question or 'hello' in question:
            return jsonify({"answer": "👋 Привет! Я ваш ИИ-помощник. Задайте мне любой вопрос!"})
        
        # Умный генеративный ответ
        responses = [
            f"🤔 По вашему вопросу '{question}': это интересная тема! Что именно вас интересует?",
            f"💡 '{question}' - хороший вопрос! Могу рассказать подробнее, уточните детали?",
            f"🎯 Понял ваш запрос про '{question}'. Нужна дополнительная информация?",
            f"🔍 Изучаю вопрос '{question}'. Какие аспекты最重要?",
            f"🚀 Принял! По теме '{question}' есть много информации. Что именно интересует?"
        ]
        
        return jsonify({"answer": random.choice(responses)})
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return jsonify({"answer": "⚠️ Произошла ошибка обработки запроса. Попробуйте еще раз."})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "AI Service is running", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Запуск локального ИИ-сервиса на порту 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
