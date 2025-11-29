# 🌐 Guía de Despliegue con Dominio y HTTPS

Esta guía te ayudará a poner tu aplicación en línea con un dominio personalizado y conexión segura HTTPS.

## 📋 Opciones de Despliegue

### Opción 1: Desarrollo Local con HTTPS (Rápido)

Para probar HTTPS en tu máquina local:

```bash
# 1. Instalar dependencia para generar certificados
pip install cryptography

# 2. Generar certificados SSL auto-firmados
python generate_ssl.py

# 3. Iniciar servidor HTTPS
python app_secure.py
```

Accede a: `https://localhost:5000`

⚠ **Nota**: Tu navegador mostrará una advertencia porque el certificado es auto-firmado. Esto es normal para desarrollo.

---

### Opción 2: Tunneling con ngrok (Sin necesidad de servidor)

ngrok crea un túnel HTTPS público hacia tu servidor local:

```bash
# 1. Descargar ngrok desde https://ngrok.com/download
# 2. Crear cuenta gratuita en ngrok.com
# 3. Instalar y autenticar

# 4. Iniciar tu servidor Flask normal
python app.py

# 5. En otra terminal, crear túnel HTTPS
ngrok http 5000
```

ngrok te dará una URL pública tipo: `https://abc123.ngrok.io`

✅ **Ventajas**:
- HTTPS automático
- No necesitas comprar dominio
- Perfecto para demos y pruebas

❌ **Desventajas**:
- La URL cambia cada vez que reinicias ngrok (gratis)
- Límites de tráfico en plan gratuito

---

### Opción 3: Despliegue en la Nube (Producción)

#### A) Render.com (Recomendado - Gratis)

1. **Crear cuenta en [Render.com](https://render.com)**

2. **Preparar tu proyecto**:
   - Sube tu código a GitHub
   - Asegúrate de tener `requirements.txt`

3. **Crear Web Service en Render**:
   - New > Web Service
   - Conecta tu repositorio de GitHub
   - Configuración:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Environment**: Python 3

4. **Añadir gunicorn**:
   ```bash
   # Agregar a requirements.txt
   gunicorn==21.2.0
   ```

5. **Dominio personalizado**:
   - En Render Dashboard > Settings > Custom Domains
   - Agregar tu dominio
   - Configurar DNS en tu proveedor de dominio

✅ **Ventajas**:
- HTTPS automático y gratuito
- Dominio incluido (.onrender.com)
- Fácil de configurar
- Plan gratuito generoso

#### B) Railway.app

Similar a Render, también ofrece despliegue gratuito con HTTPS automático.

```bash
# 1. Instalar Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Iniciar proyecto
railway init

# 4. Desplegar
railway up
```

#### C) PythonAnywhere

1. Crear cuenta en [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Subir archivos o clonar desde GitHub
3. Configurar Web App
4. HTTPS incluido en todos los planes

---

### Opción 4: Servidor VPS Propio

Para control total, usa un VPS (DigitalOcean, Linode, AWS, etc.)

#### Requisitos:
- Servidor Ubuntu/Debian
- Dominio propio
- SSH access

#### Configuración Completa:

```bash
# 1. Conectar por SSH
ssh root@tu-servidor-ip

# 2. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 3. Instalar Python y dependencias
sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx -y

# 4. Clonar tu proyecto
cd /var/www
git clone https://github.com/tu-usuario/descargardeyt.git
cd descargardeyt

# 5. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 6. Configurar Nginx
sudo nano /etc/nginx/sites-available/descargardeyt

# Contenido:
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/descargardeyt/static;
    }

    client_max_body_size 100M;
}

# 7. Habilitar sitio
sudo ln -s /etc/nginx/sites-available/descargardeyt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 8. Obtener certificado SSL GRATIS de Let's Encrypt
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# 9. Crear servicio systemd para mantener app corriendo
sudo nano /etc/systemd/system/descargardeyt.service

# Contenido:
[Unit]
Description=Descargar de YT
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/descargardeyt
Environment="PATH=/var/www/descargardeyt/venv/bin"
ExecStart=/var/www/descargardeyt/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target

# 10. Iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable descargardeyt
sudo systemctl start descargardeyt
sudo systemctl status descargardeyt
```

---

## 🌍 Registrar un Dominio

### Proveedores recomendados:

1. **Namecheap** - ~$10/año
2. **Google Domains** - ~$12/año
3. **Cloudflare** - ~$10/año + CDN gratis
4. **GoDaddy** - ~$15/año
5. **.es domains** - ~$8/año

### Configurar DNS:

Una vez tengas tu dominio, configura los registros DNS:

```
Tipo: A
Nombre: @
Valor: [IP de tu servidor]

Tipo: A
Nombre: www
Valor: [IP de tu servidor]
```

---

## 🔒 Certificado SSL Gratis

### Let's Encrypt (Recomendado)

Certbot instala y renueva automáticamente certificados SSL gratuitos:

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado (automático con Nginx)
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Renovación automática (ya configurada)
sudo certbot renew --dry-run
```

---

## 📊 Monitoreo y Mantenimiento

### Ver logs en producción:

```bash
# Logs de la aplicación
sudo journalctl -u descargardeyt -f

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Actualizar aplicación:

```bash
cd /var/www/descargardeyt
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart descargardeyt
```

---

## 🛡️ Seguridad Adicional

### Firewall (UFW):

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### Fail2ban (Protección contra ataques):

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 💰 Costos Aproximados

| Opción | Costo Mensual | Costo Anual |
|--------|---------------|-------------|
| ngrok (Free) | $0 | $0 |
| Render (Free) | $0 | $0 |
| Railway (Free) | $0 | $0 |
| Dominio | ~$1 | ~$10 |
| VPS Básico (DigitalOcean) | $5 | $60 |
| **Total Mínimo** | **$5-6** | **$60-70** |

---

## ✅ Resumen de Pasos

1. **Desarrollo Local**: Usa `python app.py`
2. **HTTPS Local**: Usa `generate_ssl.py` + `app_secure.py`
3. **Demo Rápida**: Usa ngrok
4. **Producción Gratis**: Usa Render.com o Railway
5. **Producción Pro**: VPS + Nginx + Let's Encrypt

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs
2. Verifica configuración DNS (puede tardar 24-48h)
3. Asegúrate de que el puerto 5000 esté libre
4. Verifica que ffmpeg esté instalado

---

**Desarrollado con 💜 por brussj**
