#!/bin/bash
export TELEGRAM_TOKEN="8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"
nohup python3 ~/cloud-api/bot.py > ~/cloud-api/bot.log 2>&1 &
echo "Бот запущен! Логи: ~/cloud-api/bot.log"
