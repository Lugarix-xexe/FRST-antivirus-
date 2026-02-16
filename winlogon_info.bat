@echo off
echo ====== ПАРАМЕТРЫ WINLOGON ======
echo.
echo --- Путь к исполняемому файлу ---
dir %systemroot%\System32\winlogon.exe
echo.
echo --- Ключи реестра Winlogon ---
reg query HKLM\Temp_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
echo.
echo --- Текущий процесс winlogon ---
tasklist /fi "imagename eq winlogon.exe"