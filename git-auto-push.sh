#!/bin/bash
# Настраиваем git для автоматического подтверждения
git config --global core.sshCommand "ssh -o StrictHostKeyChecking=accept-new"

cd ~/cloud-api

# Пушим
git push origin main
