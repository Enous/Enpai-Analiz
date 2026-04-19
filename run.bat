@echo off
chcp 65001 >nul
title Açık Kaynak Analiz Uygulaması - Electron Baslatici
echo [1/2] Bagimliliklar kontrol ediliyor...
if not exist node_modules (
    echo node_modules bulunamadi, kuruluyor...
    npm install
)
echo.
echo [2/2] Açık Kaynak Analiz Uygulaması Baslatiliyor...
npm start
