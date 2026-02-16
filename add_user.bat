@echo off
net user %1 %2 /add
net localgroup Users %1 /add
echo Пользователь %1 добавлен.