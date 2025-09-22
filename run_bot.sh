#!/bin/bash

# Переменная с токеном (замени на свой)
export TELEGRAM_TOKEN="8253068855:AAFPNJke9PYju90RgZe4ZOKOuuMSJNAs0X8"

# Запуск бота в фоне с логами
nohup python3 ~/cloud-api/bot.py > ~/cloud-api/bot.log 2>&1 &
echo "Бот запущен! Логи: ~/cloud-api/bot.log"
