@echo off
chcp 866 >NUL
SET PYTHONUNBUFFERED=TRUE
start cmd /k python12\python.exe menu.py
