# Script para hacer deploy a Render
Set-Location "c:\Users\bruno\OneDrive\Documentos\descargardepags"

Write-Host "=== DEPLOY A RENDER ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Verificando estado de Git..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "2. Agregando archivos..." -ForegroundColor Yellow
git add app.py

Write-Host ""
Write-Host "3. Haciendo commit..." -ForegroundColor Yellow
git commit -m "Integrar Cobalt API para YouTube - solucion definitiva a bloqueos"

Write-Host ""
Write-Host "4. Subiendo a GitHub..." -ForegroundColor Yellow
git push origin master

Write-Host ""
Write-Host "=== DEPLOY COMPLETADO ===" -ForegroundColor Green
Write-Host "Render detectará el cambio y desplegará automáticamente en 3-5 minutos" -ForegroundColor Green
Write-Host ""
Write-Host "Verifica el deploy en: https://dashboard.render.com/" -ForegroundColor Cyan
