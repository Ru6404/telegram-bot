import os
from openai import AsyncOpenAI
import asyncio

async def test_openai():
    # Проверяем переменные окружения
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key exists: {bool(api_key)}")
    print(f"Key starts with: {api_key[:10]}... if exists")
    
    if not api_key:
        print("❌ OPENAI_API_KEY не найден!")
        return
    
    client = AsyncOpenAI(api_key=api_key)
    
    try:
        print("🔍 Тестируем подключение к OpenAI...")
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Привет! Ответь коротко, что такое ИИ?"}],
            max_tokens=100
        )
        print("✅ OpenAI работает отлично!")
        print("📝 Ответ:", response.choices[0].message.content)
    except Exception as e:
        print("❌ Ошибка OpenAI:", e)
        print("🔧 Тип ошибки:", type(e).__name__)

if __name__ == "__main__":
    asyncio.run(test_openai())
