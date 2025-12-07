# 🎬 Descargador Universal de Videos y Audio

Aplicación web profesional para descargar videos y música de **más de 1000 plataformas** con interfaz moderna, sistema anti-bloqueo avanzado y soporte completo para YouTube 4K/8K.

## ✨ Características Principales

### 🎥 Descargas Avanzadas
- 🎬 **Videos hasta 8K** (4320p) con detección automática de calidades disponibles
- 🎞️ **Calidades YouTube**: 4K (2160p), 2K (1440p), Full HD (1080p), HD (720p), SD (480p), 360p
- 🎵 **Audio de alta calidad** en múltiples formatos (MP3, M4A, OPUS)
- 🖼️ **Miniaturas/Portadas HD** con conversión automática (JPG, PNG, WebP)

### 🚀 Tecnología Anti-Bloqueo
- ⚡ **Cobalt API v9** integrada para YouTube (evita bloqueos de IP)
- 🔄 **User-Agent rotativo** (pool de 6 agentes para evitar detección)
- 💾 **Sistema de caché inteligente** (1 hora TTL, reduce peticiones repetidas)
- 🍪 **Soporte completo de cookies** (acceso a contenido privado/restringido)
- 🌐 **Múltiples APIs de respaldo** (Invidious, Piped) para máxima disponibilidad
- 🖥️ **Node.js integrado** para resolver challenges de YouTube (formatos premium)

### 🌍 Compatibilidad Universal
- 📱 **1000+ plataformas soportadas** vía yt-dlp
- 🎯 **Optimizaciones específicas** para YouTube, SoundCloud, Vimeo, Instagram, TikTok
- 🔗 **Detección automática** de plataforma y mejor método de descarga
- 📊 **Tamaños de archivo estimados** con precisión (bitrate × duración)

### 🎨 Interfaz Moderna
- 💫 **Diseño glassmorphism** con animaciones fluidas
- 🌈 **Gradientes dinámicos** y efectos visuales profesionales
- 📱 **Totalmente responsive** (móvil, tablet, desktop)
- 🔍 **Búsqueda en tiempo real** de 1000+ plataformas soportadas
- ⚡ **Feedback instantáneo** de progreso y estados

## 🛠️ Requisitos del Sistema

### Esenciales
- **Python 3.8+** (recomendado 3.11)
- **FFmpeg** (conversiones y merge de audio/video)
- **Node.js 20+** (opcional pero recomendado para YouTube 4K)

### Instalación de Dependencias

**FFmpeg:**
```bash
# Windows (Chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg
```

**Node.js (para YouTube 4K):**
```bash
# Windows (Chocolatey)
choco install nodejs

# macOS
brew install node

# Linux
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## 📦 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/ssjbru/descarga-audio-y-video.git
cd descarga-audio-y-video

# 2. Instalar dependencias Python
pip install -r requirements.txt

# 3. Iniciar servidor
python app.py
```

Accede a: `http://localhost:5000`

## 🚀 Despliegue en Producción

### Opción 1: Render.com (Recomendado - Gratis)

1. **Sube código a GitHub**
2. **Conecta con Render**: https://render.com
3. **Configuración automática** vía `render.yaml`
4. **Deploy en 3-5 minutos** con Node.js y FFmpeg incluidos

**Características incluidas:**
- ✅ HTTPS automático (certificado SSL gratuito)
- ✅ Dominio gratuito `.onrender.com`
- ✅ Node.js instalado automáticamente (para YouTube 4K)
- ✅ FFmpeg preinstalado
- ✅ 750 horas gratis/mes

### Opción 2: Railway.app

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Opción 3: VPS Personalizado

Ver guía completa en `DEPLOY_GUIDE.md`

## 💻 Uso de la Aplicación

### Descargar Videos/Audio

1. **Pega la URL** del contenido que deseas descargar
2. **Click en "Obtener Formatos"** → análisis automático del video
3. **Selecciona la pestaña:**
   - 🎬 **Video** - Múltiples calidades disponibles
   - 🎵 **Audio** - Solo audio en alta calidad
   - 🖼️ **Portada** - Miniatura en alta resolución
4. **Elige calidad específica** (4K, 2K, 1080p, etc.)
5. **Descarga** → archivo listo en segundos

### Características Avanzadas

**Recortar Video:**
- Selecciona inicio y fin con timeline interactivo
- Previsualización en tiempo real
- Mantén la calidad original

**Convertir Formato:**
- Sube cualquier video/audio
- Convierte a MP4, MP3, M4A, WebM, etc.
- Procesamiento rápido con FFmpeg

**Subir y Procesar:**
- Recorta videos locales
- Convierte formatos sin perder calidad
- Interfaz drag & drop

## 🌐 Plataformas Soportadas (1000+)

### ⭐ Optimizadas con Cobalt API
- **YouTube** - Hasta 8K, todas las calidades, anti-bloqueo avanzado
- **YouTube Music** - Audio en alta calidad

### ✅ Totalmente Compatibles
- **Redes Sociales**: Instagram (Reels, Stories), TikTok, Twitter/X, Facebook
- **Streaming**: Vimeo, Dailymotion, Twitch (VODs/Clips)
- **Música**: SoundCloud, Bandcamp, Mixcloud, Spotify (vía YouTube)
- **Educación**: Udemy, Coursera, Khan Academy
- **Adultos**: Pornhub, XNXX, XVideos, YouPorn
- **Y 1000+ más...**

### ❌ NO Soportadas (DRM)
- Netflix, Disney+, HBO Max, Amazon Prime Video (protección DRM)
- Spotify/Apple Music directo (usa YouTube para buscar la misma canción)
## 📁 Arquitectura del Proyecto

```
descarga-audio-y-video/
├── app.py                    # 🔥 Backend Flask con sistema anti-bloqueo
├── app_secure.py             # 🔒 Servidor HTTPS con SSL
├── external_4k_api.py        # 🌐 APIs externas (Invidious/Piped) para 4K
├── requirements.txt          # 📦 Dependencias Python
├── render.yaml              # ☁️ Configuración Render.com
├── render-build.sh          # 🛠️ Script de build (Node.js + FFmpeg)
├── DEPLOY_GUIDE.md          # 📘 Guía completa de despliegue
├── COOKIES_SETUP.md         # 🍪 Configuración de cookies avanzada
├── templates/
│   └── index.html           # 🎨 Interfaz HTML moderna
├── static/
│   ├── style.css            # 💫 Estilos con glassmorphism
│   ├── script.js            # ⚡ Lógica frontend
│   └── translations.js      # 🌍 Soporte multiidioma
└── downloads/               # 💾 Archivos temporales (auto-limpieza)
```

## 🔧 Tecnologías Implementadas

### Backend (Python/Flask)
- **Flask 3.1.2** - Framework web ligero y potente
- **yt-dlp 2025.11.12** - Descargador universal (1000+ plataformas)
- **Cobalt API v9** - Sistema anti-bloqueo para YouTube
- **Requests** - Cliente HTTP con soporte cookies
- **Gunicorn** - Servidor WSGI para producción

### Optimizaciones Anti-Bloqueo
- 🔄 **User-Agent Rotation**: Pool de 6 agentes rotativos
- 💾 **Metadata Caching**: Cache en memoria (TTL 1h)
- 🍪 **Cookie Management**: Soporte completo cookies YouTube
- 🌐 **Multi-API Strategy**: Cobalt → Invidious → Piped → yt-dlp
- 🖥️ **Node.js Runtime**: Resolve YouTube signature challenges

### Frontend (HTML5/CSS3/JS)
- **Vanilla JavaScript** (sin frameworks, ultra rápido)
- **CSS Moderno**: Glassmorphism, gradientes, animaciones
- **Responsive Design**: Mobile-first approach
- **Fetch API**: Peticiones asíncronas nativas

## 🎯 Características Técnicas Avanzadas

### Sistema de Caché Inteligente
```python
# Cache automático de metadata (1 hora TTL)
video_metadata_cache = {
    'video_id': {
        'formats': [...],
        'duration': 183,
        'timestamp': 1733524800
    }
}
```

### User-Agent Rotation
```python
USER_AGENTS = [
    'Chrome 120.0.0.0 Windows',
    'Chrome 119.0.0.0 Windows', 
    'Chrome 120.0.0.0 macOS',
    'Chrome 120.0.0.0 Linux',
    'Firefox 121.0 Windows',
    'Safari 17.1 macOS'
]
```

### Estrategia Multi-API
1. **Cobalt API** → Prioridad para YouTube (anti-bloqueo)
2. **yt-dlp** → Detección de calidades disponibles
3. **Invidious API** → Fallback para formatos premium
4. **Piped API** → Alternativa si Invidious falla
5. **Fallback Estándar** → Muestra todas las calidades

### Estimación Precisa de Tamaños
```python
bitrate_estimates = {
    2160: {'video': 12.0, 'audio': 0.128},  # 4K
    1440: {'video': 8.0, 'audio': 0.128},   # 2K
    1080: {'video': 5.0, 'audio': 0.128},   # Full HD
    720: {'video': 2.5, 'audio': 0.128},    # HD
    480: {'video': 1.0, 'audio': 0.128},    # SD
    360: {'video': 0.5, 'audio': 0.128},    # Low
}
filesize = (bitrate_mbps * duration * 1000000) / 8
```

## 💰 Costos de Despliegue

| Plataforma | Costo Mensual | HTTPS | Dominio | Node.js | FFmpeg | Límites |
|------------|---------------|-------|---------|---------|--------|---------|
| **Render.com** | Gratis | ✅ Auto | ✅ .onrender.com | ✅ | ✅ | 750h/mes |
| **Railway** | Gratis | ✅ Auto | ✅ .railway.app | ✅ | ✅ | $5 crédito |
| **Vercel** | Gratis | ✅ Auto | ✅ .vercel.app | ✅ | ❌ | 100GB/mes |
| **Heroku** | $5+ | ✅ Auto | ✅ .herokuapp.com | ✅ | ⚠️ Buildpack | Sin tier gratis |
| **VPS (DigitalOcean)** | $6/mes | ⚙️ Manual | ⚙️ Comprar | ✅ | ✅ | Ilimitado |
| **Local (ngrok)** | Gratis | ✅ Auto | ✅ Temporal | ✅ | ✅ | Sin persistencia |

**Recomendación:** 🏆 **Render.com** - Setup automático, Node.js incluido, 750h gratis suficiente.

## ⚠️ Limitaciones Conocidas

### YouTube 4K/8K
- 🔒 **Protección YouTube**: Bloqueos agresivos a formatos premium
- 🖥️ **Requiere Node.js**: Para resolver signature challenges
- 🍪 **Cookies recomendadas**: Mejora acceso a 4K
- ⚡ **Cobalt API ayuda**: Pero no garantiza 100% éxito
- 📝 **Fallback**: Si no hay 4K, descarga mejor calidad disponible

### Restricciones de Plataformas
- 🌍 **Geo-restricciones**: Algunos videos no disponibles en tu región
- 👤 **Contenido privado**: Requiere cookies con sesión autenticada  
- ⏱️ **Rate limiting**: YouTube puede limitar descargas masivas
- 📺 **DRM protegido**: Netflix, Spotify, etc. imposible de descargar

### Rendimiento
- 📦 **Videos grandes**: 4K/8K tardan más (tamaño real)
- 🔄 **Primera descarga**: Cache vacío, más lento
- ⚡ **Después de cache**: 10x más rápido (1 hora TTL)
- 🌐 **APIs externas**: Timeout 5s, pueden fallar

## 🐛 Solución de Problemas

### ❌ Error: "FFmpeg not found"
```bash
# Verificar instalación
ffmpeg -version

# Si no está instalado:
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg  
# Linux: sudo apt install ffmpeg

# Asegurarte que esté en PATH
echo $env:PATH  # Windows PowerShell
echo $PATH      # Linux/macOS
```

### ❌ Error: "No se detecta 4K"
```bash
# 1. Verificar Node.js
node --version  # Debe ser v20+

# 2. Verificar cookies
ls /etc/secrets/www.youtube.com_cookies  # Render
ls youtube_cookies.txt                    # Local

# 3. Ver logs
[COBALT] ✓ Node.js disponible: v22.16.0  # ← Debe aparecer
[COBALT] ✓ Calidades finales: [2160, 1440, ...]  # ← Debe incluir 2160

# 4. Si sigue sin funcionar: es limitación de YouTube
# La app muestra 4K, Cobalt intenta descargarlo
```

### ❌ Error: "Requested format not available"
```bash
# Normal en algunos videos, usa fallback automático
# La app mostrará 6 calidades estándar

# Solución: Elegir otra calidad (1080p, 720p)
```

### ❌ Error: "HTTP 429 Too Many Requests"
```bash
# YouTube detectó demasiadas peticiones

# Solución:
# 1. Esperar 10-15 minutos
# 2. Usar cookies autenticadas
# 3. Cache ayuda (evita repetir requests)
```

### ⚡ El sitio está lento
```bash
# 1. Render free tier: servidor duerme tras 15min inactividad
# Primera petición tarda ~30s (cold start)

# 2. Usar cache:
# Buscar el mismo video 2 veces
# Segunda vez: instantáneo

# 3. Upgrade a Render Paid: $7/mes sin cold starts
```

## 📝 Licencia y Uso Responsable

### Licencia
Este proyecto es de código abierto bajo **Licencia MIT**.
- ✅ Uso comercial permitido
- ✅ Modificación y distribución libre
- ✅ Uso privado sin restricciones
- ⚠️ Sin garantía ni responsabilidad del autor

### ⚖️ Uso Legal y Ético

**IMPORTANTE: Esta herramienta es solo para uso personal y educativo.**

#### ✅ Usos Permitidos:
- Descargar contenido de dominio público
- Guardar tus propios videos subidos
- Contenido con licencia Creative Commons
- Material educativo con permiso del autor
- Backups personales de contenido adquirido legalmente

#### ❌ Usos NO Permitidos:
- Piratería o redistribución comercial
- Violar términos de servicio de plataformas
- Descargar contenido protegido sin permiso
- Uso masivo automatizado (scraping)

#### 📜 Responsabilidad Legal:
**El usuario es 100% responsable del uso de esta herramienta.**
- Respeta los derechos de autor en tu jurisdicción
- Cumple los términos de servicio de YouTube y otras plataformas
- Usa descargas solo para uso personal no comercial
- El desarrollador NO se hace responsable del mal uso

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! 

### Cómo Contribuir:
1. **Fork** este repositorio
2. **Crea una rama**: `git checkout -b feature/nueva-funcionalidad`
3. **Commit cambios**: `git commit -m 'Agregar nueva funcionalidad'`
4. **Push a tu fork**: `git push origin feature/nueva-funcionalidad`
5. **Abre Pull Request** con descripción detallada

### Áreas de Mejora:
- 🎨 Mejoras UI/UX
- 🚀 Optimizaciones de rendimiento
- 🐛 Corrección de bugs
- 📝 Documentación y traducciones
- 🔧 Nuevas funcionalidades

## 📧 Soporte y Contacto

### Documentación:
- 📘 **Guía de Despliegue**: `DEPLOY_GUIDE.md`
- 🍪 **Configuración Cookies**: `COOKIES_SETUP.md`
- ⚡ **Deploy Rápido**: `QUICK_DEPLOY.md`

### Recursos Externos:
- **yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **FFmpeg**: https://ffmpeg.org/documentation.html
- **Cobalt API**: https://github.com/wukko/cobalt
- **Flask**: https://flask.palletsprojects.com/

### Comunidad:
- 🐛 **Reportar Bugs**: [GitHub Issues](https://github.com/ssjbru/descarga-audio-y-video/issues)
- 💡 **Sugerencias**: [GitHub Discussions](https://github.com/ssjbru/descarga-audio-y-video/discussions)
- ⭐ **Dale Star**: Si te gusta el proyecto

## 🎯 Roadmap Futuro

### Próximas Características:
- [ ] 🎬 **Descargas por lotes** (múltiples URLs)
- [ ] 📱 **App móvil nativa** (React Native)
- [ ] 🔐 **Sistema de cuentas** (historial de descargas)
- [ ] 📊 **Dashboard de analytics** (estadísticas de uso)
- [ ] 🌍 **Más idiomas** (español, inglés, portugués, francés)
- [ ] ⚡ **Worker queues** (descargas en segundo plano)
- [ ] 🎨 **Temas personalizables** (modo oscuro/claro)
- [ ] 📂 **Integración cloud** (Google Drive, Dropbox)

### Mejoras Técnicas Planeadas:
- [ ] 🔄 **WebSockets** para progreso en tiempo real
- [ ] 💾 **Redis cache** para mejor rendimiento
- [ ] 🐳 **Docker** para despliegue simplificado
- [ ] 🧪 **Tests unitarios** (pytest)
- [ ] 📈 **Monitoring** (Sentry, Datadog)

---

## 🌟 Agradecimientos

Gracias a los desarrolladores de:
- **yt-dlp** - Motor principal de descargas
- **FFmpeg** - Procesamiento de video/audio
- **Cobalt** - API anti-bloqueo para YouTube
- **Flask** - Framework web Python
- **Render.com** - Hosting gratuito confiable

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella en GitHub ⭐**

Hecho con ❤️ para la comunidad open source

[🏠 Inicio](#-descargador-universal-de-videos-y-audio) • [📦 Instalación](#-instalación-rápida) • [🚀 Despliegue](#-despliegue-en-producción) • [📝 Licencia](#-licencia-y-uso-responsable)

</div>
