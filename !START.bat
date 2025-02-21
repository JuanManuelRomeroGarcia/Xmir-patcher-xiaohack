@echo off
chcp 65001 >NUL
SET PYTHONUNBUFFERED=TRUE

if not exist "python12\python.exe" (
    echo Error: No se encontró python.exe en la carpeta python12.
    pause
    exit
)

start cmd /k python12\python.exe menu.py || pause
