@echo off
echo Анализ MBR (требуется дополнительное ПО, здесь только проверка наличия буткитов)
echo.
echo Загрузочные записи на диске 0:
wmic partition get DeviceID, BlockSize, StartingOffset, Size, Type
echo.
echo Проверка через bootsect (если доступно):
if exist %systemroot%\System32\bootsect.exe (
    bootsect /nt60 SYS /mbr
) else (
    echo bootsect не найден.
)