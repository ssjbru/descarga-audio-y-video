@echo off
cd /d "c:\Users\bruno\OneDrive\Documentos\descargardepags"

echo === DEPLOY A RENDER (CON MEJORAS VISUALES) ===
echo.

echo 1. Estado de Git...
git status

echo.
echo 2. Agregando archivos...
git add app.py static/script.js static/style.css

echo.
echo 3. Commit...
git commit -m "Feature: Obtener tamanos REALES de YouTube con yt-dlp (como ssyt.rip)"

echo.
echo 4. Push a GitHub...
git push origin master

echo.
echo === COMPLETADO ===
echo Render desplegara en 3-5 minutos
echo Nueva funcionalidad:
echo - Tamanios REALES obtenidos de YouTube (sin estimaciones)
echo - Usa yt-dlp en modo metadata (rapido, sin descargar)
echo - Muestra el tamano exacto de cada calidad
echo - Fallback a "Variable" si no puede obtener tamanios
echo - Animaciones de entrada suaves
echo - Hover effects mejorados
pause
