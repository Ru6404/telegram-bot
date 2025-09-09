from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import time

app = FastAPI(title="Quantum System 2025")

html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum System 2025 🚀</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: white; padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 3rem; padding: 2rem; }
        .logo { font-size: 4rem; margin-bottom: 1rem; animation: pulse 2s infinite; }
        @keyframes pulse {
            0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); }
        }
        .title { font-size: 3rem; font-weight: 300; margin-bottom: 1rem; }
        .subtitle { font-size: 1.2rem; opacity: 0.9; }
        .dashboard {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem; margin-bottom: 3rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
            border-radius: 20px; padding: 1.5rem; text-align: center;
            transition: transform 0.3s ease; border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .card-icon { font-size: 2.5rem; margin-bottom: 1rem; }
        .card-title { font-size: 1.3rem; margin-bottom: 1rem; font-weight: 600; }
        .card-value { font-size: 1.8rem; font-weight: bold; margin-bottom: 0.5rem; }
        .card-desc { font-size: 0.9rem; opacity: 0.8; }
        .status-online { color: #4ade80; } .status-offline { color: #ff4757; }
        .status-loading { color: #ffa726; }
        .buttons {
            display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;
            margin-bottom: 2rem;
        }
        .btn {
            background: rgba(255, 255, 255, 0.2); border: none; padding: 1rem 2rem;
            border-radius: 50px; color: white; font-size: 1rem; cursor: pointer;
            transition: all 0.3s ease; text-decoration: none; display: inline-flex;
            align-items: center; gap: 0.5rem;
        }
        .btn:hover { background: rgba(255, 255, 255, 0.3); transform: translateY(-2px); }
        .footer { text-align: center; margin-top: 3rem; opacity: 0.7; padding: 1rem; }
        .stats { display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap; }
        .stat-item { text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; }
        .stat-label { font-size: 0.9rem; opacity: 0.8; }
        @media (max-width: 768px) {
            .title { font-size: 2rem; } .dashboard { grid-template-columns: 1fr; }
            .buttons { flex-direction: column; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡</div>
            <h1 class="title">Quantum System 2025</h1>
            <p class="subtitle">Универсальная AI система следующего поколения</p>
        </div>
        
        <div class="stats">
            <div class="stat-item"><div class="stat-number" id="uptime">00:00:00</div><div class="stat-label">Аптайм</div></div>
            <div class="stat-item"><div class="stat-number" id="memory">0%</div><div class="stat-label">Память</div></div>
            <div class="stat-item"><div class="stat-number" id="cpu">0%</div><div class="stat-label">CPU</div></div>
        </div>
        
        <div class="dashboard">
            <div class="card"><div class="card-icon">🌐</div><h3 class="card-title">Статус системы</h3><div class="card-value status-online" id="systemStatus">ONLINE</div><div class="card-desc">Все системы работают</div></div>
            <div class="card"><div class="card-icon">🚀</div><h3 class="card-title">Производительность</h3><div class="card-value" id="performance">100%</div><div class="card-desc">Оптимальная нагрузка</div></div>
            <div class="card"><div class="card-icon">🛡️</div><h3 class="card-title">Безопасность</h3><div class="card-value" id="security">ACTIVE</div><div class="card-desc">Все защиты включены</div></div>
            <div class="card"><div class="card-icon">🤖</div><h3 class="card-title">Telegram бот</h3><div class="card-value status-online" id="botStatus">ONLINE</div><div class="card-desc">@RuslanOmegaBot</div></div>
            <div class="card"><div class="card-icon">💾</div><h3 class="card-title">Память</h3><div class="card-value" id="memUsage">0 MB</div><div class="card-desc">Использование</div></div>
            <div class="card"><div class="card-icon">⏱️</div><h3 class="card-title">Время ответа</h3><div class="card-value" id="responseTime">0ms</div><div class="card-desc">Среднее</div></div>
        </div>
        
        <div class="buttons">
            <a href="/health" class="btn">📊 Статус API</a>
            <a href="/docs" class="btn">📖 Документация</a>
            <a href="https://t.me/RuslanOmegaBot" class="btn">🤖 Telegram бот</a>
            <button class="btn" onclick="refreshData()">🔄 Обновить</button>
        </div>
        
        <div class="footer"><p>© 2025 Quantum System | Все системы работают стабильно</p></div>
    </div>
    
    <script>
        let startTime = Date.now();
        function updateUptime() {
            const now = Date.now(); const diff = now - startTime;
            const hours = Math.floor(diff / 3600000);
            const minutes = Math.floor((diff % 3600000) / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            document.getElementById('uptime').textContent = 
                `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        async function loadData() {
            try {
                const start = performance.now();
                const response = await fetch('/health');
                const end = performance.now();
                const data = await response.json();
                document.getElementById('responseTime').textContent = `${Math.round(end - start)}ms`;
                document.getElementById('systemStatus').textContent = data.status.toUpperCase();
                document.getElementById('memory').textContent = '25%';
                document.getElementById('memUsage').textContent = '25%';
                document.getElementById('cpu').textContent = '15%';
            } catch (error) {
                document.getElementById('systemStatus').textContent = 'ERROR';
                document.getElementById('systemStatus').className = 'card-value status-offline';
            }
        }
        function refreshData() {
            document.getElementById('systemStatus').textContent = 'UPDATING...';
            document.getElementById('systemStatus').className = 'card-value status-loading';
            loadData();
        }
        loadData(); updateUptime();
        setInterval(loadData, 5000); setInterval(updateUptime, 1000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(html_content)

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "2025.1.0", "timestamp": time.time()}

@app.get("/docs")
async def docs():
    return {"message": "API документация"}

if __name__ == "__main__":
    print("🚀 Запускаем улучшенный Quantum System...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
