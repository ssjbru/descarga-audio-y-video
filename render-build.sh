#!/usr/bin/env bash
# Script de construcción para Render.com

set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Instalar ffmpeg y Node.js (necesario para yt-dlp challenges de YouTube)
apt-get update
apt-get install -y ffmpeg

# Instalar Node.js 20.x para resolver challenges de YouTube (4K)
echo "Instalando Node.js para desbloquear formatos 4K..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Verificar instalación
node --version
npm --version
