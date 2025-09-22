#!/bin/bash
echo "Бот запущен! Логи: ~/cloud-api/bot.log"
nohup python3 ~/cloud-api/bot.py > ~/cloud-api/bot.log 2>&1 &
