@echo off
net user %1 /active:no
echo Пользователь %1 заблокирован.