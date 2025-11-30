#!/usr/bin/env bash
# Script de construcción para Render.com

set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Instalar ffmpeg
apt-get update
apt-get install -y ffmpeg
