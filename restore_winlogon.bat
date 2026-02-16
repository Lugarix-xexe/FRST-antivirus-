@echo off
echo Восстановление параметров Winlogon по умолчанию...
reg add "HKLM\Temp_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Shell /t REG_SZ /d "explorer.exe" /f
reg add "HKLM\Temp_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v Userinit /t REG_SZ /d "C:\Windows\system32\userinit.exe," /f
echo Готово.