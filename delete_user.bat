@echo off
net user %1 /delete
echo Пользователь %1 удалён (если существовал).