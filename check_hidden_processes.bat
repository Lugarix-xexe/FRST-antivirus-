@echo off
echo Сравнение списков процессов (возможны скрытые):
echo ================================================
echo Запущенные процессы (tasklist):
tasklist
echo.
echo Проверка через WMIC (может показать больше):
wmic process get name,processid