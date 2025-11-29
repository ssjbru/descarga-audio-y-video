# 🎬 Descargador Universal de Videos y Audio

Aplicación web para descargar videos y música de **más de 1000 plataformas** con interfaz moderna, segura y animada.

## ✨ Características

- 🎬 **Descarga de videos** en múltiples resoluciones (desde 144p hasta 4K/8K)
- 🎵 **Descarga de audio** en diferentes calidades (MP3, M4A, OPUS)
- 🖼️ **Descarga de miniaturas/portadas** con conversión de formato (JPG, PNG, WebP)
- 🌐 **Soporte para 1000+ plataformas**: YouTube, Instagram, TikTok, Vimeo, SoundCloud, Twitter/X, Facebook, y muchas más
- 📊 **Visualización de formatos disponibles** con tamaño de archivo
- 💾 **Selección de calidad personalizada**
- 🎨 **Interfaz moderna** con animaciones, glassmorphism y gradientes
- 🔍 **Búsqueda de plataformas soportadas** con más de 1000 extractores
- 🔒 **Versión segura con HTTPS** incluida
- ⚡ **Descarga rápida y eficiente**

## 🛠️ Requisitos Previos

- Python 3.8 o superior
- FFmpeg (recomendado para mejor compatibilidad y conversiones)

### Instalar FFmpeg

**Windows:**
1. Descarga FFmpeg desde: https://ffmpeg.org/download.html
2. Extrae el archivo y añade la carpeta `bin` al PATH del sistema
3. O usa Chocolatey: `choco install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 📦 Instalación

1. **Clona o descarga este proyecto**

2. **Instala las dependencias de Python:**
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### Desarrollo Local (HTTP)
```bash
python app.py
```
Accede a: `http://localhost:5000`

### Desarrollo Local con HTTPS
```bash
# 1. Instalar dependencias adicionales
pip install cryptography

# 2. Generar certificados SSL auto-firmados
python generate_ssl.py

# 3. Iniciar servidor seguro
python app_secure.py
```
Accede a: `https://localhost:5000`

⚠ El navegador mostrará advertencia (certificado auto-firmado). Haz clic en "Avanzado" > "Continuar a localhost".

### 🌐 Despliegue con Dominio

#### Opción 1: ngrok (Demo Rápida)
```bash
# Descarga ngrok desde https://ngrok.com
# Inicia tu servidor
python app.py

# En otra terminal
ngrok http 5000
```
Obtendrás una URL HTTPS pública: `https://abc123.ngrok.io`

#### Opción 2: Render.com (Gratis + Dominio)
1. Sube tu código a GitHub
2. Crea cuenta en [Render.com](https://render.com)
3. New > Web Service > Conecta GitHub
4. ¡Listo! Obtienes HTTPS + dominio `.onrender.com`

#### Opción 3: VPS Propio
Ver guía completa en `DEPLOY_GUIDE.md`

## 💻 Uso de la Aplicación

1. **Pega el enlace** del video o música que quieres descargar
2. **Haz clic en "Obtener Formatos"**
3. **Selecciona la pestaña** deseada:
   - 🎬 **Video** - Descargar video en diferentes calidades
   - 🎵 **Audio** - Extraer solo el audio en MP3/M4A
   - 🖼️ **Portada** - Descargar miniatura/portada
4. **Elige la calidad** que prefieras
5. **Haz clic en "Descargar"**

## 🌐 Plataformas Soportadas

Esta aplicación utiliza `yt-dlp`, que soporta **más de 1000 plataformas**, incluyendo:

### ✨ Plataformas Optimizadas:
- **YouTube** - Videos en todas las calidades (144p hasta 4K/8K)
- **SoundCloud** - Música y podcasts (solo audio)
- **Vimeo** - Videos profesionales y creativos
- **Instagram** - Reels, posts, IGTV
- **TikTok** - Videos cortos

### ✅ Otras Plataformas Soportadas:
- Facebook, Twitter (X), Reddit
- Dailymotion, Twitch (clips y VODs)
- Bandcamp (música), Mixcloud
- Pornhub, XNXX, XVideos, YouPorn
- Y **1000+ plataformas más**...

Haz clic en **"Ver Todas las Plataformas"** en la web para ver la lista completa con búsqueda.

### ❌ Plataformas NO Soportadas (protección DRM):
- Spotify, Apple Music (usa YouTube para buscar la misma canción)
- Netflix, Disney+, HBO Max, Amazon Prime Video

## 📁 Estructura del Proyecto

```
descargardeyt/
├── app.py                 # Servidor Flask backend (HTTP)
├── app_secure.py          # Servidor Flask con HTTPS
├── generate_ssl.py        # Generador de certificados SSL
├── requirements.txt       # Dependencias Python
├── DEPLOY_GUIDE.md        # Guía completa de despliegue
├── COOKIES_SETUP.md       # Configuración de cookies
├── templates/
│   └── index.html        # Interfaz HTML
├── static/
│   ├── style.css         # Estilos CSS con animaciones
│   └── script.js         # Lógica JavaScript
├── ssl/                  # Certificados SSL (se crea al generar)
│   ├── cert.pem
│   └── key.pem
└── downloads/            # Carpeta temporal (se crea automáticamente)
```

## 🔒 Seguridad

### Headers de Seguridad Incluidos:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy`

### Protección de Datos:
- Los archivos descargados se almacenan temporalmente
- Eliminación automática después de 1 hora
- Cada descarga tiene un ID único para evitar conflictos
- Cookies seguras en modo HTTPS
- Protección contra XSS y CSRF

## ⚙️ Configuración

### Variables de Configuración en `app.py`:

- **Puerto del servidor**: Por defecto es `5000`
- **Tiempo de limpieza de archivos**: 1 hora (3600 segundos)
- **Carpeta de descargas**: `downloads/`
- **Cookies de YouTube**: `youtube_cookies.txt` (opcional)

### Configuración SSL/HTTPS:

Ver `DEPLOY_GUIDE.md` para instrucciones completas sobre:
- Certificados auto-firmados (desarrollo)
- Let's Encrypt (producción)
- Configuración de dominio
- Despliegue en VPS/Cloud

## 💰 Costos de Despliegue

| Opción | Costo | HTTPS | Dominio |
|--------|-------|-------|---------|
| Local | Gratis | ✅ Auto-firmado | ❌ localhost |
| ngrok | Gratis | ✅ Incluido | ✅ Subdomain |
| Render.com | Gratis | ✅ Incluido | ✅ .onrender.com |
| Railway | Gratis | ✅ Incluido | ✅ .railway.app |
| VPS + Dominio | ~$5-6/mes | ✅ Let's Encrypt | ✅ Propio |

## ⚠️ Limitaciones y Notas

- **Uso legal**: Solo descarga contenido del cual tengas permiso o que sea de dominio público
- **Derechos de autor**: Respeta las leyes de derechos de autor de tu país
- **Rendimiento**: Las descargas de alta calidad pueden tardar más tiempo
- **FFmpeg recomendado**: Mejora la compatibilidad y permite conversiones

## 🐛 Solución de Problemas

### Error: "FFmpeg not found"
- Asegúrate de haber instalado FFmpeg y que esté en el PATH del sistema
- Reinicia tu terminal/PowerShell después de instalar FFmpeg

### Error: "No se pudo descargar"
- Verifica que la URL sea válida
- Algunos videos pueden tener restricciones regionales
- Intenta con una calidad diferente

### El servidor no inicia
- Verifica que el puerto 5000 no esté en uso
- Asegúrate de haber instalado todas las dependencias: `pip install -r requirements.txt`

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún error o quieres agregar nuevas características, siéntete libre de abrir un issue o pull request.

## 📧 Soporte

Si tienes problemas o preguntas, puedes:
- Revisar la documentación de yt-dlp: https://github.com/yt-dlp/yt-dlp
- Verificar que FFmpeg esté correctamente instalado
- Asegurarte de tener la última versión de Python

---

**Nota importante**: Esta herramienta es solo para uso personal y educativo. Respeta siempre los términos de servicio de las plataformas y las leyes de derechos de autor.
