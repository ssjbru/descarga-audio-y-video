# 🚀 Guía de Deploy en Render.com (GRATIS)

Esta guía te ayudará a desplegar tu aplicación en Render.com con un dominio gratuito y HTTPS automático.

## 📋 Requisitos previos

- ✅ Cuenta de GitHub (gratis)
- ✅ Cuenta de Render.com (gratis)
- ✅ Tu código ya está listo para deploy

## 🔧 Paso 1: Subir el código a GitHub

### 1.1 Crear repositorio en GitHub
1. Ve a https://github.com y haz login
2. Haz clic en el botón **"+"** arriba a la derecha → **"New repository"**
3. Nombre del repositorio: `descargador-universal` (o el que prefieras)
4. Configura como **Public** o **Private**
5. **NO** marques "Add a README file"
6. Haz clic en **"Create repository"**

### 1.2 Subir tu código
Abre PowerShell en tu carpeta del proyecto y ejecuta:

```powershell
# Inicializar Git (si no lo has hecho)
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Preparar app para deploy en Render"

# Conectar con tu repositorio de GitHub (reemplaza TU-USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU-USUARIO/descargador-universal.git

# Subir el código
git branch -M main
git push -u origin main
```

**Nota:** Si git te pide autenticación, usa tu token de acceso personal de GitHub.

## 🌐 Paso 2: Deploy en Render.com

### 2.1 Crear cuenta en Render
1. Ve a https://render.com
2. Haz clic en **"Get Started"** o **"Sign Up"**
3. Usa **"Sign up with GitHub"** para conectar tu cuenta

### 2.2 Crear nuevo Web Service
1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub:
   - Si es la primera vez, autoriza a Render para acceder a tus repos
   - Busca tu repositorio `descargador-universal`
   - Haz clic en **"Connect"**

### 2.3 Configurar el servicio
Render detectará automáticamente que es una app Python. Configura así:

**Configuración básica:**
- **Name:** `descargador-universal` (será parte de tu URL)
- **Region:** Elige el más cercano (ej: Frankfurt, Oregon)
- **Branch:** `main`
- **Root Directory:** (déjalo vacío)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 300`

**Plan:**
- Selecciona **"Free"** (gratuito)

### 2.4 Variables de entorno (Opcional)
Si necesitas configurar algo especial, agrega variables en **"Environment"**

### 2.5 Desplegar
1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu app
3. Esto tomará 5-10 minutos la primera vez

## ✅ Paso 3: Acceder a tu aplicación

Una vez que el deploy termine (verás "Live" en verde):

Tu aplicación estará disponible en:
```
https://descargador-universal.onrender.com
```

**Características incluidas:**
- ✅ HTTPS automático (certificado SSL real)
- ✅ Dominio gratuito
- ✅ Auto-deploy cuando hagas push a GitHub
- ✅ Logs en tiempo real

## 🔄 Actualizaciones futuras

Para actualizar tu app después de hacer cambios:

```powershell
# Hacer cambios en tu código
# Luego:
git add .
git commit -m "Descripción de los cambios"
git push
```

Render automáticamente detectará el push y re-desplegará tu app.

## ⚠️ Limitaciones del plan gratuito

- La app se "duerme" después de 15 minutos de inactividad
- El primer acceso después de dormir puede tardar 30-60 segundos
- 750 horas gratis por mes (suficiente para uso personal)
- Ancho de banda limitado

## 🎯 Dominios personalizados

Si en el futuro compras un dominio (ej: `miapp.com`):

1. Ve a tu servicio en Render
2. Haz clic en **"Settings"** → **"Custom Domains"**
3. Agrega tu dominio
4. Configura los registros DNS según las instrucciones de Render

## 🐛 Solución de problemas

### La app no inicia
1. Revisa los logs en el dashboard de Render
2. Verifica que `requirements.txt` tenga todas las dependencias
3. Asegúrate de que `Procfile` y `render.yaml` estén correctos

### Error con yt-dlp
- yt-dlp se actualiza frecuentemente
- Si hay errores, actualiza la versión en `requirements.txt`

### La carpeta downloads no funciona
- Render tiene almacenamiento efímero
- Los archivos se borran al reiniciar
- Es normal para este tipo de app de descarga temporal

## 📞 Soporte

- Documentación de Render: https://render.com/docs
- Comunidad de Render: https://community.render.com

## 🎉 ¡Listo!

Ahora tienes tu aplicación corriendo en internet con:
- 🌐 Dominio gratuito
- 🔒 HTTPS automático
- 🚀 Deploy automático desde GitHub
- 💰 100% gratis
