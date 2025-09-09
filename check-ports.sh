#!/bin/bash
echo "🔍 ПРОВЕРКА ЗАНЯТЫХ ПОРТОВ"

echo "Порты 8000-8100:"
for port in {8000..8100}; do
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        echo "❌ Порт $port занят"
    else
        echo "✅ Порт $port свободен"
    fi
done

echo ""
echo "🎯 Рекомендуемые свободные порты:"
netstat -tuln 2>/dev/null | grep -q ":8080 " || echo "👉 8080"
netstat -tuln 2>/dev/null | grep -q ":8081 " || echo "👉 8081" 
netstat -tuln 2>/dev/null | grep -q ":8001 " || echo "👉 8001"
