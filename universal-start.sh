#!/bin/bash
# ==================== УНИВЕРСАЛЬНЫЙ АВТОЗАПУСК ====================

EMAIL="ruslan6404kim@gmail.com"
CLOUD_API_DIR="$HOME/cloud-api"

echo "🌐 Универсальный запуск Cloud API для: $EMAIL"

# Функция проверки и установки
setup_cloud_api() {
    echo "🔍 Проверяем установку Cloud API..."
    
    if [ ! -d "$CLOUD_API_DIR" ]; then
        echo "📦 Cloud API не найден, устанавливаем..."
        download_cloud_api
    fi
    
    cd "$CLOUD_API_DIR"
    install_dependencies
    start_server
}

# Функция загрузки с GitHub
download_cloud_api() {
    echo "📥 Загружаем Cloud API с GitHub..."
    
    if command -v git &> /dev/null; then
        git clone https://github.com/Ru6404/cloud-api.git "$CLOUD_API_DIR"
    else
        echo "❌ Git не установлен. Установите: apt-get install git / brew install git"
        exit 1
    fi
    
    if [ ! -d "$CLOUD_API_DIR" ]; then
        echo "❌ Ошибка загрузки. Создаем базовую структуру..."
        create_basic_structure
    fi
}

# Создание базовой структуры
create_basic_structure() {
    mkdir -p "$CLOUD_API_DIR"
    cd "$CLOUD_API_DIR"
    
    cat > main.py << 'EOF'
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Auto-Cloud API", version="1.0")

@app.get("/")
async def root():
    return {"message": "🚀 Auto-Cloud API запущен!", "email": "ruslan6404kim@gmail.com"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
EOF

    cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
EOF
}

# Установка зависимостей
install_dependencies() {
    echo "📦 Проверяем зависимости..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 не установлен"
        install_python
    fi
    
    if ! python3 -c "import fastapi" 2>/dev/null; then
        echo "📦 Устанавливаем FastAPI..."
        pip3 install -r requirements.txt || pip install -r requirements.txt
    fi
}

# Установка Python
install_python() {
    echo "🐍 Устанавливаем Python..."
    
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y python3 python3-pip
    elif command -v brew &> /dev/null; then
        # MacOS
        brew install python
    else
        echo "❌ Не могу установить Python автоматически"
        exit 1
    fi
}

# Запуск сервера
start_server() {
    echo "🚀 Запускаем сервер..."
    cd "$CLOUD_API_DIR"
    
    # Проверяем, не запущен ли уже
    if pgrep -f "uvicorn main:app" > /dev/null; then
        echo "✅ Сервер уже запущен"
        show_status
        return
    fi
    
    # Запускаем в фоне
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
    
    echo "⏳ Ожидаем запуск..."
    sleep 3
    
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "🎉 Сервер запущен успешно!"
        show_status
    else
        echo "❌ Ошибка запуска. Смотри server.log"
        cat server.log
    fi
}

# Показать статус
show_status() {
    echo ""
    echo "📊 СТАТУС СИСТЕМЫ:"
    echo "👉 Email: $EMAIL"
    echo "🌐 URL: http://localhost:8000"
    echo "📁 Директория: $CLOUD_API_DIR"
    echo ""
    echo "🚀 КОМАНДЫ ДЛЯ УПРАВЛЕНИЯ:"
    echo "  curl http://localhost:8000/          - Главная страница"
    echo "  curl http://localhost:8000/health    - Статус здоровья"
    echo "  tail -f $CLOUD_API_DIR/server.log    - Просмотр логов"
    echo ""
}

# Основная логика
main() {
    echo "🔧 УСТАНОВКА CLOUD API ДЛЯ: $EMAIL"
    echo "💻 Устройство: $(hostname)"
    echo "🌐 ОС: $(uname -s)"
    echo ""
    
    setup_cloud_api
}

# Запуск
main "$@",v
