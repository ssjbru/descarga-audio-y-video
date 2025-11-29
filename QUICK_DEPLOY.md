# 🚀 GUÍA RÁPIDA DE DESPLIEGUE

## Opción Recomendada: Render.com (Más Fácil)

### ✅ Ventajas:
- ✅ **100% Gratis** para empezar
- ✅ **HTTPS automático** incluido
- ✅ **Dominio gratuito** (.onrender.com)
- ✅ **Despliegue automático** desde GitHub
- ✅ **No requiere tarjeta de crédito**

### 📋 Pasos:

#### 1. Subir a GitHub

```bash
# Inicializar Git (si no lo has hecho)
git init
git add .
git commit -m "Initial commit"

# Crear repositorio en GitHub.com
# Luego:
git remote add origin https://github.com/TU-USUARIO/descargardeyt.git
git push -u origin main
```

#### 2. Desplegar en Render

1. **Ve a [Render.com](https://render.com)** y crea cuenta gratuita
2. Click en **"New +"** > **"Web Service"**
3. **Conecta tu GitHub** y selecciona el repositorio
4. **Configuración automática detectada:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Dejar todo lo demás por defecto
5. Click en **"Create Web Service"**
6. **¡Espera 2-3 minutos!** ⏳

#### 3. ¡Listo! 🎉

Tu app estará en: `https://tu-app.onrender.com`

#### 4. Dominio Personalizado (Opcional)

En Render Dashboard:
1. **Settings** > **Custom Domains**
2. Click **"Add Custom Domain"**
3. Ingresa tu dominio: `tudominio.com`
4. Configura DNS en tu proveedor:
   ```
   CNAME record:
   Name: www
   Value: tu-app.onrender.com
   
   A record:
   Name: @
   Value: [IP que Render te dé]
   ```

---

## Opción Avanzada: VPS Propio

### 💰 Costo: ~$5-6/mes

**Proveedores recomendados:**
- [DigitalOcean](https://digitalocean.com) - $6/mes
- [Linode](https://linode.com) - $5/mes  
- [Vultr](https://vultr.com) - $5/mes
- [Contabo](https://contabo.com) - €4/mes (más barato)

### 📋 Pasos Detallados:

#### 1. Crear VPS (Droplet)

1. Crea cuenta en DigitalOcean
2. Create > Droplets
3. Configuración:
   - **OS**: Ubuntu 22.04 LTS
   - **Plan**: Basic $6/mes (1GB RAM)
   - **Datacenter**: Closest to you
4. Añade tu SSH key (recomendado)
5. Click "Create Droplet"

#### 2. Conectar por SSH

```bash
# Desde tu terminal local
ssh root@TU_IP_DEL_VPS

# Si usas Windows sin SSH, descarga PuTTY
```

#### 3. Instalar Todo Automáticamente

```bash
# Copiar archivos al servidor (desde tu PC local)
scp -r * root@TU_IP_DEL_VPS:/var/www/descargardeyt/

# En el servidor VPS
cd /var/www/descargardeyt
chmod +x setup_server.sh
./setup_server.sh
```

#### 4. Configurar Nginx

```bash
# Editar configuración
sudo nano /etc/nginx/sites-available/descargardeyt

# Pegar (reemplaza TU_DOMINIO.com):
```

```nginx
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
        expires 30d;
    }

    client_max_body_size 100M;
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/descargardeyt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Configurar Servicio Systemd

```bash
# Crear directorio de logs
sudo mkdir -p /var/log/descargardeyt
sudo chown www-data:www-data /var/log/descargardeyt

# Copiar archivo de servicio
sudo cp descargardeyt.service /etc/systemd/system/

# Iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable descargardeyt
sudo systemctl start descargardeyt
sudo systemctl status descargardeyt
```

#### 6. Obtener HTTPS Gratis (Let's Encrypt)

```bash
# Instalar certificado SSL (reemplaza tu dominio)
sudo certbot --nginx -d tudominio.com -d www.tudominio.com

# Certbot configurará HTTPS automáticamente
# Renovación automática ya está configurada
```

#### 7. Configurar DNS de tu Dominio

En tu proveedor de dominio (Namecheap, GoDaddy, etc.):

```
Tipo: A
Nombre: @
Valor: [IP_DE_TU_VPS]
TTL: 300

Tipo: A  
Nombre: www
Valor: [IP_DE_TU_VPS]
TTL: 300
```

**⏳ Espera 5-30 minutos** para que DNS se propague.

---

## 🔍 Verificar que Funciona

```bash
# Ver logs en tiempo real
sudo journalctl -u descargardeyt -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/access.log

# Verificar estado del servicio
sudo systemctl status descargardeyt

# Reiniciar servicio
sudo systemctl restart descargardeyt
```

---

## 🔄 Actualizar Aplicación

```bash
cd /var/www/descargardeyt
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart descargardeyt
```

---

## 🛡️ Seguridad Adicional

### Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

### Fail2ban

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 💰 Comparación de Costos

| Opción | Mensual | Anual | HTTPS | Dominio |
|--------|---------|-------|-------|---------|
| **Render.com** | **$0** | **$0** | ✅ Incluido | ✅ .onrender.com |
| Railway.app | $0 | $0 | ✅ Incluido | ✅ .railway.app |
| VPS + Dominio | $5-6 | $60-70 | ✅ Let's Encrypt | ✅ Propio (~$10/año) |

---

## 🌍 Comprar Dominio

**Recomendados:**
- [Namecheap](https://namecheap.com) - ~$10/año
- [Cloudflare](https://cloudflare.com) - ~$10/año + CDN gratis
- [Porkbun](https://porkbun.com) - ~$8/año

---

## 📞 Soporte

Si tienes problemas:

1. **Render no funciona:**
   - Revisa logs en Render Dashboard
   - Verifica que requirements.txt esté correcto

2. **VPS no funciona:**
   - `sudo systemctl status descargardeyt`
   - `sudo journalctl -u descargardeyt -n 50`
   - Verifica que DNS esté configurado correctamente

3. **Dominio no resuelve:**
   - Espera 24-48h para propagación DNS
   - Verifica con: `nslookup tudominio.com`

---

## ✅ Checklist Final

- [ ] Código subido a GitHub
- [ ] Cuenta en Render.com creada
- [ ] Web Service desplegado
- [ ] App funcionando en .onrender.com
- [ ] Dominio comprado (opcional)
- [ ] DNS configurado (opcional)
- [ ] HTTPS funcionando

---

**Desarrollado con 💜 por brussj**

¿Problemas? Abre un issue en GitHub o revisa los logs.
