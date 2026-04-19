@echo off
title Enpai Analiz - Kurulum ve Baslatma
echo [1/2] Bagimliliklar kontrol ediliyor...
pip install -r requirements.txt
echo.
echo [2/2] Enpai Analiz baslatiliyor...
python file_organizer.py
pause
