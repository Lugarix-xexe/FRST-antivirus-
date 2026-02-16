@echo off
chcp 65001 >nul
echo ========================================
echo    MTTUnlocker - Антивирус для WinRE
echo ========================================
echo.
echo Убедитесь, что вы указали правильный диск с Windows
echo (обычно C:), после запуска программы.
echo.
cd /d %~dp0
if exist antivirus.exe (
    start "" "antivirus.exe"
) else (
    echo Ошибка: antivirus.exe не найден в текущей папке.
    pause
)