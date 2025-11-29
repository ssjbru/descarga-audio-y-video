@echo off
echo ================================================
echo   Descargador Universal - By brussj
echo   Iniciando servidor HTTP...
echo ================================================
echo.

cd /d "%~dp0"

if exist "entorno.venv\Scripts\activate.bat" (
    echo [+] Activando entorno virtual...
    call entorno.venv\Scripts\activate.bat
) else (
    echo [!] No se encontro entorno virtual, usando Python del sistema
)

echo.
echo [+] Iniciando servidor en http://localhost:5000
echo [!] Presiona Ctrl+C para detener el servidor
echo.

python app.py

pause
