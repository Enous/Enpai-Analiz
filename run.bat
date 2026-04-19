@echo off
title Enpai Analiz - Electron Baslatici
echo [1/2] Bagimliliklar kontrol ediliyor...
if not exist node_modules (
    echo node_modules bulunamadi, kuruluyor...
    npm install
)
echo.
echo [2/2] Enpai Analiz Baslatiliyor...
npm start
