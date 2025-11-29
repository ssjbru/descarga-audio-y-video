#!/bin/bash

# Script de configuración inicial para servidor VPS
# Ejecutar como root o con sudo

echo "================================================"
echo "  Instalando dependencias del sistema..."
echo "================================================"

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx ffmpeg git

echo ""
echo "✓ Dependencias instaladas"
echo ""
echo "================================================"
echo "  Configurando aplicación..."
echo "================================================"

# Crear directorio
mkdir -p /var/www/descargardeyt
cd /var/www/descargardeyt

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Aplicación configurada"
echo ""
echo "================================================"
echo "  Siguiente paso: Configurar Nginx"
echo "================================================"
echo ""
echo "Crea el archivo de configuración:"
echo "  sudo nano /etc/nginx/sites-available/descargardeyt"
echo ""
echo "Y pega esta configuración (reemplaza TU_DOMINIO.com):"
echo ""
echo "---------------------------------------------------"
cat << 'EOF'
server {
    listen 80;
    server_name TU_DOMINIO.com www.TU_DOMINIO.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/descargardeyt/static;
        expires 30d;
    }

    client_max_body_size 100M;
}
EOF
echo "---------------------------------------------------"
echo ""
echo "Luego ejecuta:"
echo "  sudo ln -s /etc/nginx/sites-available/descargardeyt /etc/nginx/sites-enabled/"
echo "  sudo nginx -t"
echo "  sudo systemctl restart nginx"
echo ""
