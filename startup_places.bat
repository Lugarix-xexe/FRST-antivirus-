@echo off
set drive=%1
echo ========== АВТОЗАГРУЗКА ==========
echo.
echo --- Реестр: HKLM\Temp_SOFTWARE\Microsoft\Windows\CurrentVersion\Run ---
reg query HKLM\Temp_SOFTWARE\Microsoft\Windows\CurrentVersion\Run 2>nul
echo.
echo --- Реестр: HKCU\Software\Microsoft\Windows\CurrentVersion\Run ---
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run 2>nul
echo.
echo --- Папки Startup (все пользователи) ---
dir "%drive%\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup" 2>nul
echo.
echo --- Папки Startup (текущий пользователь) ---
dir "%drive%\Users\%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" 2>nul
echo.
echo --- Планировщик задач (первые 20) ---
schtasks /query /fo LIST /nh | findstr /i "TaskName" 2>nul
echo.
echo --- Службы, запускающиеся автоматически ---
sc query type= service state= all | findstr /i "SERVICE_NAME.*AUTO_START"
echo.
echo --- Winlogon (Shell, Userinit) ---
reg query HKLM\Temp_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon 2>nul
echo.
echo --- AppInit_DLLs ---
reg query HKLM\Temp_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows 2>nul | findstr /i "AppInit"