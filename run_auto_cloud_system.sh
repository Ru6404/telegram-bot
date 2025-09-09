#!/data/data/com.termux/files/usr/bin/bash
# Запуск всей системы Auto-Cloud

cd /data/data/com.termux/files/home/cloud-api

echo "🚀 Запуск Auto-Cloud API..."
python main.py &

echo "⏳ Ждем запуска API..."
sleep 3

echo "🤖 Запуск Auto-Cloud Bot..."
python auto_cloud_bot.py
