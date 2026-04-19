@echo off
chcp 65001 >nul
title Enpai-Dev Analiz Kurulumu
color 0B

echo =========================================
echo Enpai-Dev Analiz - Gereksinim Kurulumu
echo =========================================
echo.

:: Check if npm is installed
where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [HATA] Node.js veya npm sisteminizde kurulu degil!
    echo Lutfen https://nodejs.org adresinden Node.js'i indirin ve kurun.
    echo.
    pause
    exit /b 1
)

echo [BiLGi] npm bulundu. Gerekli paketler (Electron, fs-extra vb.) kuruluyor...
echo Lutfen bekleyin, bu islem internet hiziniza bagli olarak biraz surebilir...
echo.

call npm install

if %ERRORLEVEL% equ 0 (
    echo.
    echo [BASARILI] Tum gereksinimler basariyla kuruldu!
    echo Artik uygulamayi baslatmak icin 'run.bat' dosyasini calistirabilirsiniz.
) else (
    echo.
    echo [HATA] Kurulum sirasinda bir sorun olustu. Lutfen internet baglantinizi veya hata kodunu kontrol edin.
)

echo.
pause
