@echo off
set drive=%1
set file=%2
set quarantine_dir=%drive%\quarantine
if not exist %quarantine_dir% mkdir %quarantine_dir%
move "%file%" "%quarantine_dir%"
echo Файл перемещён в карантин: %quarantine_dir%