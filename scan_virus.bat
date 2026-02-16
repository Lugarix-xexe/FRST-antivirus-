@echo off
set drive=%1
echo Запуск сканирования на вирусы (используется сигнатурный поиск или ClamAV)
echo.
if exist "C:\Program Files\ClamAV\clamscan.exe" (
    "C:\Program Files\ClamAV\clamscan.exe" -r %drive%\
) else (
    echo ClamAV не установлен. Выполняю поиск известных вредоносных файлов...
    echo Поиск файлов с подозрительными именами...
    dir /s /b %drive%\*virus*.exe %drive%\*trojan*.exe %drive%\*backdoor*.exe 2>nul
)