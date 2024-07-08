@echo off
if "%~1"=="" (
    echo Uso: %0 archivo.cody
    exit /b 1
)
python main.py %1