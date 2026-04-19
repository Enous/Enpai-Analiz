@echo off
:: Encoding fix
chcp 65001 >nul
title Enpai Dev Analiz - Launcher

echo ==========================================
echo       ENPAI DEV ANALIZ BASLATILIYOR
echo ==========================================
echo.
echo [1/2] Kontroller yapiliyor...

:: Check node_modules
if not exist node_modules (
    echo [!] Bagimliliklar eksik, kuruluyor...
    call npm install
)

echo.
echo [2/2] Uygulama aciliyor...
:: Start Electron
call npm start

if %ERRORLEVEL% neq 0 (
    echo.
    echo [X] Bir hata olustu!
    echo Lutfen node.js kurulu oldugundan emin olun.
    pause
)
