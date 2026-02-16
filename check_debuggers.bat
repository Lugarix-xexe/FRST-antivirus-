@echo off
echo ====== ДЕБАГГЕРЫ И РУТКИТЫ ======
echo.
echo --- Image File Execution Options (возможные отладчики) ---
reg query HKLM\Temp_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options 2>nul
echo.
echo --- Проверка скрытых процессов (пример) ---
wmic process get name,processid | findstr /i "cmd.exe powershell.exe"
echo.
echo --- Проверка на наличие руткитов (базовая) ---
echo Сравнение процессов в userspace и kernel...