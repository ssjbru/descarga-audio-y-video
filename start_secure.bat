@echo off
echo ================================================
echo   Descargador Universal - By brussj
echo   Iniciando servidor HTTPS seguro...
echo ================================================
echo.

cd /d "%~dp0"

if exist "entorno.venv\Scripts\activate.bat" (
    echo [+] Activando entorno virtual...
    call entorno.venv\Scripts\activate.bat
) else (
    echo [!] No se encontro entorno virtual, usando Python del sistema
)

if not exist "ssl\cert.pem" (
    echo.
    echo [!] No se encontraron certificados SSL
    echo [+] Generando certificados auto-firmados...
    echo.
    python generate_ssl.py
    echo.
)

echo.
echo [+] Iniciando servidor HTTPS en https://localhost:5000
echo [!] Tu navegador mostrara una advertencia de seguridad
echo [!] Haz clic en "Avanzado" y luego "Continuar a localhost"
echo [!] Presiona Ctrl+C para detener el servidor
echo.

python app_secure.py

pause
