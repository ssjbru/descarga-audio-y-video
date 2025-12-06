from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import json
from pathlib import Path
import uuid
import threading
import time
import subprocess
import shutil
import tempfile
import requests
import re

app = Flask(__name__)

# Configuración para permitir archivos grandes sin límite
app.config['MAX_CONTENT_LENGTH'] = None  # Sin límite de tamaño

# Configuración de cacheo para archivos estáticos
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # No cachear en desarrollo

# Carpeta para descargas temporales - Por defecto en disco local
# El usuario puede cambiarla desde la interfaz
DEFAULT_DOWNLOAD_FOLDER = os.path.join('C:\\', 'Temp', 'descargardepags')
DOWNLOAD_FOLDER = DEFAULT_DOWNLOAD_FOLDER

# Buscar cookies en múltiples ubicaciones
COOKIES_FILE = None
COOKIES_FILE_WRITABLE = None  # Copia escribible para yt-dlp

possible_cookie_paths = [
    '/etc/secrets/www.youtube.com_cookies',  # Render Secret Files (nuevo)
    '/etc/secrets/youtube_cookies.txt',  # Render Secret Files (anterior)
    os.path.join(os.getcwd(), 'www.youtube.com_cookies'),  # Carpeta actual (nuevo)
    os.path.join(os.getcwd(), 'youtube_cookies.txt'),  # Carpeta actual
    'www.youtube.com_cookies',  # Relativo (nuevo)
    'youtube_cookies.txt'  # Relativo
]
for path in possible_cookie_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        COOKIES_FILE = path
        print(f"✓ Archivo de cookies encontrado en: {path}")
        
        # Si el archivo es de solo lectura (como en Render), copiarlo a temp
        try:
            # Intentar abrir en modo append para verificar si es escribible
            with open(path, 'a'):
                pass
            # Si funciona, usar directamente
            COOKIES_FILE_WRITABLE = path
            print(f"  → Cookies usables directamente (escribible)")
        except (IOError, OSError):
            # Si falla, copiar a archivo temporal escribible
            try:
                temp_dir = tempfile.gettempdir()
                temp_cookies = os.path.join(temp_dir, 'youtube_cookies_temp.txt')
                shutil.copy2(path, temp_cookies)
                COOKIES_FILE_WRITABLE = temp_cookies
                print(f"  → Cookies copiadas a ubicación escribible: {temp_cookies}")
            except Exception as e:
                print(f"  ⚠ No se pudo copiar cookies: {e}")
                COOKIES_FILE_WRITABLE = None
        break

if not COOKIES_FILE:
    print("⚠ No se encontraron cookies. Para evitar bloqueos de YouTube: Lee las instrucciones en COOKIES_SETUP.md")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Diccionario para almacenar el progreso de las descargas
download_progress = {}

# Configuración de Cobalt API
COBALT_API_URL = "https://api.cobalt.tools/api/json"

def download_with_cobalt(url, quality='max'):
    """
    Descarga videos usando Cobalt API (para YouTube principalmente)
    Retorna la URL de descarga directa o None si falla
    """
    try:
        print(f"[COBALT] Intentando descargar con Cobalt API: {url}")
        print(f"[COBALT] Calidad solicitada: {quality}")
        
        payload = {
            "url": url,
            "vQuality": quality,  # max, 2160, 1440, 1080, 720, 480, 360
            "filenamePattern": "basic",
            "isAudioOnly": False,
            "disableMetadata": False
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        print(f"[COBALT] Payload: {payload}")
        response = requests.post(COBALT_API_URL, json=payload, headers=headers, timeout=30)
        
        print(f"[COBALT] Código de respuesta: {response.status_code}")
        print(f"[COBALT] Respuesta completa: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            print(f"[COBALT] Estado: {status}")
            
            if status == 'redirect' or status == 'stream':
                download_url = data.get('url')
                if download_url:
                    print(f"[COBALT] ✓ URL de descarga obtenida: {download_url[:100]}...")
                    return download_url
                else:
                    print(f"[COBALT] ✗ No hay URL en la respuesta")
                    print(f"[COBALT] Datos completos: {data}")
                    return None
            elif status == 'picker':
                # Múltiples opciones (videos de carrusel, etc)
                picker = data.get('picker', [])
                if picker:
                    download_url = picker[0].get('url')
                    print(f"[COBALT] ✓ URL de descarga obtenida (picker): {download_url[:100]}...")
                    return download_url
                else:
                    print(f"[COBALT] ✗ Picker vacío")
                    return None
            elif status == 'error':
                error_text = data.get('text', 'Error desconocido')
                print(f"[COBALT] ✗ Error de Cobalt: {error_text}")
                return None
            else:
                print(f"[COBALT] ✗ Estado no manejado: {status}")
                print(f"[COBALT] Datos completos: {data}")
                return None
        else:
            print(f"[COBALT] ✗ Error HTTP {response.status_code}")
            print(f"[COBALT] Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"[COBALT] ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def download_with_cobalt_audio(url):
    """
    Descarga solo audio usando Cobalt API
    """
    try:
        print(f"[COBALT] Descargando audio con Cobalt API: {url}")
        
        payload = {
            "url": url,
            "isAudioOnly": True,
            "filenamePattern": "basic",
            "disableMetadata": False
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        print(f"[COBALT] Payload audio: {payload}")
        response = requests.post(COBALT_API_URL, json=payload, headers=headers, timeout=30)
        
        print(f"[COBALT] Código de respuesta audio: {response.status_code}")
        print(f"[COBALT] Respuesta audio: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status')
            print(f"[COBALT] Estado audio: {status}")
            
            if status in ['redirect', 'stream']:
                download_url = data.get('url')
                if download_url:
                    print(f"[COBALT] ✓ URL de audio obtenida: {download_url[:100]}...")
                    return download_url
                else:
                    print(f"[COBALT] ✗ No hay URL de audio en la respuesta")
                    return None
            elif status == 'error':
                error_text = data.get('text', 'Error desconocido')
                print(f"[COBALT] ✗ Error de Cobalt audio: {error_text}")
                return None
        
        print(f"[COBALT] ✗ No se pudo obtener audio")
        return None
        
    except Exception as e:
        print(f"[COBALT] ✗ Error descargando audio: {e}")
        import traceback
        traceback.print_exc()
        return None

def clean_old_files():
    """Elimina archivos con más de 1 hora"""
    while True:
        try:
            current_time = time.time()
            for filename in os.listdir(DOWNLOAD_FOLDER):
                filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                if os.path.isfile(filepath):
                    if current_time - os.path.getmtime(filepath) > 3600:  # 1 hora
                        os.remove(filepath)
        except Exception as e:
            print(f"Error limpiando archivos: {e}")
        time.sleep(600)  # Revisar cada 10 minutos

# Iniciar hilo de limpieza
cleanup_thread = threading.Thread(target=clean_old_files, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ads.txt')
def ads_txt():
    """Sirve el archivo ads.txt para Google AdSense"""
    from flask import Response
    return Response('google.com, pub-7759712886141440, DIRECT, f08c47fec0942fa0', mimetype='text/plain')

@app.route('/supported_sites')
def supported_sites():
    """Obtiene la lista completa de sitios soportados por yt-dlp"""
    try:
        extractors = yt_dlp.extractor.gen_extractors()
        sites = []
        seen = set()
        
        for extractor in extractors:
            # Obtener el nombre del sitio
            ie_name = extractor.IE_NAME
            if ie_name and ie_name not in seen and ':' not in ie_name:
                # Formatear el nombre
                display_name = ie_name.replace('_', ' ').title()
                seen.add(ie_name)
                sites.append({
                    'name': display_name,
                    'id': ie_name
                })
        
        # Ordenar alfabéticamente
        sites.sort(key=lambda x: x['name'])
        
        return jsonify({
            'total': len(sites),
            'sites': sites
        })
    except Exception as e:
        print(f"Error obteniendo sitios: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/debug/cookies', methods=['GET'])
def debug_cookies():
    """Endpoint de diagnóstico para verificar estado de cookies"""
    info = {
        'cookies_found': COOKIES_FILE is not None,
        'cookies_path': COOKIES_FILE,
        'cookies_writable_path': COOKIES_FILE_WRITABLE,
        'cookies_exists': os.path.exists(COOKIES_FILE) if COOKIES_FILE else False,
        'cookies_writable_exists': os.path.exists(COOKIES_FILE_WRITABLE) if COOKIES_FILE_WRITABLE else False,
        'is_render': os.path.exists('/opt/render'),
    }
    
    # Si hay cookies, obtener info adicional
    if COOKIES_FILE_WRITABLE and os.path.exists(COOKIES_FILE_WRITABLE):
        try:
            info['cookies_size'] = os.path.getsize(COOKIES_FILE_WRITABLE)
            with open(COOKIES_FILE_WRITABLE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                info['cookies_lines'] = len(lines)
                cookie_lines = [l for l in lines if l.strip() and not l.startswith('#')]
                info['cookies_valid_lines'] = len(cookie_lines)
                youtube_cookies = [l for l in cookie_lines if 'youtube.com' in l or '.google.com' in l]
                info['youtube_cookies_count'] = len(youtube_cookies)
        except Exception as e:
            info['cookies_error'] = str(e)
    
    return jsonify(info)

@app.route('/get_formats', methods=['POST'])
def get_formats():
    """Obtiene los formatos disponibles de un video - Compatible con 1000+ plataformas"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        # Detectar plataformas para optimizaciones específicas
        is_youtube = 'youtube.com' in url or 'youtu.be' in url
        is_soundcloud = 'soundcloud.com' in url
        is_vimeo = 'vimeo.com' in url
        
        # USAR COBALT API PARA YOUTUBE - evita bloqueos de IP completamente
        if is_youtube:
            print(f"[INFO] YouTube detectado - usando SOLO Cobalt API (sin yt-dlp)")
            try:
                # Extraer ID del video de la URL
                import re
                video_id_match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', url)
                video_id = video_id_match.group(1) if video_id_match else 'Video'
                
                print(f"[COBALT] Obteniendo información del video {video_id}...")
                
                # 1. Obtener título y autor desde YouTube oEmbed API (pública, sin autenticación)
                title = f"Video de YouTube ({video_id})"
                author = "YouTube"
                try:
                    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
                    oembed_response = requests.get(oembed_url, timeout=10)
                    if oembed_response.status_code == 200:
                        oembed_data = oembed_response.json()
                        title = oembed_data.get('title', title)
                        author = oembed_data.get('author_name', author)
                        print(f"[COBALT] ✓ Título: {title}")
                        print(f"[COBALT] ✓ Autor: {author}")
                except Exception as e:
                    print(f"[COBALT] ⚠ Error en oEmbed: {e}")
                
                # 2. Obtener duración desde múltiples fuentes (con respaldos)
                duration = 0
                
                # MÉTODO 1: yt-dlp solo para metadata (sin descargar, modo extract_flat)
                try:
                    print(f"[COBALT] Intentando yt-dlp en modo metadata...")
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'extract_flat': True,
                        'skip_download': True,
                        'socket_timeout': 10,
                    }
                    if COOKIES_FILE and os.path.exists(COOKIES_FILE):
                        ydl_opts['cookiefile'] = COOKIES_FILE
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        duration = info.get('duration', 0)
                        if duration > 0:
                            print(f"[COBALT] ✓ Duración desde yt-dlp: {duration}s")
                except Exception as e:
                    print(f"[COBALT] ⚠ yt-dlp metadata falló: {e}")
                
                # MÉTODO 2: HTML Scraping de YouTube
                if duration == 0:
                    try:
                        print(f"[COBALT] Intentando extraer del HTML de YouTube...")
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        }
                        yt_page = requests.get(f"https://www.youtube.com/watch?v={video_id}", headers=headers, timeout=10)
                        if yt_page.status_code == 200:
                            # Buscar duración en el HTML (múltiples patrones)
                            duration_patterns = [
                                r'"lengthSeconds":"(\d+)"',
                                r'lengthSeconds\\":\\"(\d+)\\"',
                                r'"length":"(\d+)"',
                            ]
                            for pattern in duration_patterns:
                                duration_matches = re.findall(pattern, yt_page.text)
                                if duration_matches:
                                    duration = int(duration_matches[0])
                                    print(f"[COBALT] ✓ Duración desde HTML: {duration}s")
                                    break
                    except Exception as e:
                        print(f"[COBALT] ⚠ Extracción HTML falló: {e}")
                
                # MÉTODO 3: Invidious como respaldo
                if duration == 0:
                    invidious_instances = [
                        f"https://inv.nadeko.net/api/v1/videos/{video_id}",
                        f"https://invidious.jing.rocks/api/v1/videos/{video_id}",
                        f"https://iv.nboeck.de/api/v1/videos/{video_id}",
                        f"https://invidious.private.coffee/api/v1/videos/{video_id}",
                    ]
                    
                    for invidious_url in invidious_instances:
                        try:
                            print(f"[COBALT] Intentando {invidious_url.split('/')[2]}...")
                            invidious_response = requests.get(invidious_url, timeout=8)
                            if invidious_response.status_code == 200:
                                invidious_data = invidious_response.json()
                                duration = invidious_data.get('lengthSeconds', 0)
                                if duration > 0:
                                    print(f"[COBALT] ✓ Duración desde Invidious: {duration}s")
                                    break
                        except Exception as e:
                            print(f"[COBALT] ⚠ Instancia {invidious_url.split('/')[2]} falló: {e}")
                            continue
                
                if duration == 0:
                    print(f"[COBALT] ⚠ No se pudo obtener duración de ninguna fuente, usando duración estimada")
                    # Como último recurso, usar una duración promedio de 3 minutos para calcular tamaños
                    duration = 180
                
                # Formatear duración correctamente
                if duration > 0:
                    mins = duration // 60
                    secs = duration % 60
                    print(f"[COBALT] 📊 Duración final: {duration}s ({mins}:{secs:02d})")
                else:
                    print(f"[COBALT] 📊 Duración final: 0s (0:00)")
                
                thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
                
                # 3. Obtener tamaños aproximados basados en duración
                # Estimaciones realistas basadas en bitrates típicos de YouTube
                def estimate_size(duration_seconds, quality_height):
                    if duration_seconds == 0:
                        return "Variable"
                    
                    # Bitrates aproximados por calidad (kbps)
                    bitrates = {
                        2160: 45000,  # 4K ~45 Mbps
                        1440: 16000,  # 2K ~16 Mbps
                        1080: 8000,   # 1080p ~8 Mbps
                        720: 5000,    # 720p ~5 Mbps
                        480: 2500,    # 480p ~2.5 Mbps
                        360: 1000     # 360p ~1 Mbps
                    }
                    
                    bitrate = bitrates.get(quality_height, 5000)
                    size_mb = (bitrate * duration_seconds) / (8 * 1024)  # Convertir a MB
                    
                    if size_mb < 1024:
                        return f"~{int(size_mb)}"  # Solo el número, el script.js agregará " MB"
                    else:
                        size_gb = size_mb / 1024
                        return f"~{int(size_gb * 1024)}"  # Convertir a MB para consistencia
                
                print(f"[COBALT] 📦 Calculando tamaños basados en duración: {duration}s...")
                
                # Ofrecer calidades de Cobalt con tamaños estimados
                formats = [
                    {'format_id': 'cobalt-max', 'ext': 'mp4', 'quality': '4K (2160p)', 'height': 2160, 'resolution': '3840x2160', 'fps': 60, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': 0, 'filesize_mb': estimate_size(duration, 2160), 'has_audio': True},
                    {'format_id': 'cobalt-1440', 'ext': 'mp4', 'quality': '2K (1440p)', 'height': 1440, 'resolution': '2560x1440', 'fps': 60, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': 0, 'filesize_mb': estimate_size(duration, 1440), 'has_audio': True},
                    {'format_id': 'cobalt-1080', 'ext': 'mp4', 'quality': 'Full HD (1080p)', 'height': 1080, 'resolution': '1920x1080', 'fps': 60, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': 0, 'filesize_mb': estimate_size(duration, 1080), 'has_audio': True},
                    {'format_id': 'cobalt-720', 'ext': 'mp4', 'quality': 'HD (720p)', 'height': 720, 'resolution': '1280x720', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': 0, 'filesize_mb': estimate_size(duration, 720), 'has_audio': True},
                    {'format_id': 'cobalt-480', 'ext': 'mp4', 'quality': 'SD (480p)', 'height': 480, 'resolution': '854x480', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': 0, 'filesize_mb': estimate_size(duration, 480), 'has_audio': True},
                    {'format_id': 'cobalt-360', 'ext': 'mp4', 'quality': 'Baja (360p)', 'height': 360, 'resolution': '640x360', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': 0, 'filesize_mb': estimate_size(duration, 360), 'has_audio': True},
                ]
                
                audio_size = estimate_size(duration, 128) if duration > 0 else "Variable"
                audio_formats = [
                    {'format_id': 'cobalt-audio', 'ext': 'm4a', 'abr': 128, 'abr_text': 'Mejor Calidad', 'acodec': 'aac', 'filesize': 0, 'filesize_mb': audio_size},
                ]
                
                # Log de tamaños estimados
                for fmt in formats:
                    print(f"[COBALT]   {fmt['quality']}: {fmt['filesize_mb']} MB")
                print(f"[COBALT]   Audio: {audio_size} MB")
                
                print(f"[COBALT] ✓ Todo listo para: {title}")
                
                return jsonify({
                    'title': title,
                    'duration': duration,
                    'thumbnail': thumbnail,
                    'formats': formats,
                    'audio_formats': audio_formats,
                    'platform': 'youtube-cobalt'
                })
                
            except Exception as e:
                print(f"[ERROR COBALT] Fallo al preparar formatos: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Error al procesar video de YouTube: {str(e)}'}), 500
        
        # Configuración base universal para todas las plataformas
        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'skip_download': True,
            'no_check_certificate': True,
            'ignoreerrors': False,
            'extract_flat': False,
            'force_generic_extractor': False,
        }
        
        # Optimizaciones específicas por plataforma
        if False:  # Ya no usamos yt-dlp para YouTube
            # Usar cliente web con cookies para evitar bloqueos de bot
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['web'],  # Solo web client con cookies
                }
            }
            
            # USAR cookies - son necesarias para evitar detección de bot
            if COOKIES_FILE_WRITABLE and os.path.exists(COOKIES_FILE_WRITABLE) and os.path.getsize(COOKIES_FILE_WRITABLE) > 0:
                ydl_opts['cookiefile'] = COOKIES_FILE_WRITABLE
                print(f"✓ Cookies de YouTube cargadas desde archivo: {COOKIES_FILE_WRITABLE}")
            else:
                print("⚠ Sin cookies - YouTube bloqueará como bot")
            
            # En servidor (Render), no intentar extraer cookies del navegador
            # Solo funciona en local donde el usuario tiene navegadores instalados
            if not os.path.exists('/opt/render'):  # No estamos en Render
                try:
                    ydl_opts['cookiesfrombrowser'] = ('chrome',)
                    print("✓ Usando cookies de Chrome automáticamente")
                except:
                    try:
                        ydl_opts['cookiesfrombrowser'] = ('firefox',)
                        print("✓ Usando cookies de Firefox automáticamente")
                    except:
                        try:
                            ydl_opts['cookiesfrombrowser'] = ('edge',)
                            print("✓ Usando cookies de Edge automáticamente")
                        except:
                            print("⚠ No se pudieron cargar cookies del navegador")
                            print("   YouTube puede tener limitaciones sin cookies")
        elif is_soundcloud:
            # SoundCloud configuración optimizada
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        elif is_vimeo:
            # Vimeo configuración optimizada
            ydl_opts['http_headers'] = {
                'Referer': 'https://vimeo.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        else:
            # Configuración genérica para TODAS las demás plataformas (1000+)
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        
        print(f"\n[INFO] Extrayendo información de: {url}")
        print(f"[INFO] Plataforma: {'YouTube' if is_youtube else 'SoundCloud' if is_soundcloud else 'Vimeo' if is_vimeo else 'Universal (yt-dlp auto-detect)'}")
        
        # Log de configuración de cookies
        if is_youtube:
            if 'cookiefile' in ydl_opts:
                print(f"[INFO] Usando cookies: {ydl_opts['cookiefile']}")
            else:
                print(f"[INFO] Sin cookies - solo formatos limitados disponibles")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Obtener título
            title = info.get('title', 'Sin título')
            duration = info.get('duration', 0)
            thumbnail = info.get('thumbnail', '')
            
            # Para YouTube, ofrecer solo mejor calidad disponible
            if is_youtube:
                real_formats = info.get('formats', [])
                print(f"[INFO] YouTube - Total formatos disponibles: {len(real_formats)}")
                
                # Solo ofrecer "Mejor Calidad Disponible" - yt-dlp elige automáticamente
                formats = [
                    {'format_id': 'best', 'ext': 'mp4', 'quality': 'Mejor Calidad Disponible', 'height': 0, 'resolution': 'Auto', 'fps': 0, 'vcodec': 'auto', 'acodec': 'auto', 'filesize': 0, 'filesize_mb': 'Variable', 'has_audio': True},
                ]
                
                audio_formats = [
                    {'format_id': 'bestaudio', 'ext': 'm4a', 'abr': 0, 'abr_text': 'Mejor Calidad', 'acodec': 'auto', 'filesize': 0, 'filesize_mb': 'Variable'},
                ]
                
                print(f"[INFO] YouTube - Descargará la mejor calidad disponible automáticamente")
            
            elif is_soundcloud:
                # SoundCloud es solo audio
                # Calcular tamaño aproximado basado en duración
                duration_min = duration / 60 if duration else 3
                
                formats = []
                audio_formats = [
                    {'format_id': 'http-128', 'ext': 'mp3', 'abr': 128, 'abr_text': '128kbps (Alta)', 'acodec': 'mp3', 'filesize': int(128 * 128 * duration_min) if duration else 0, 'filesize_mb': round(128 * 128 * duration_min / (1024 * 1024), 2) if duration else '~4-6'},
                    {'format_id': 'http-64', 'ext': 'mp3', 'abr': 64, 'abr_text': '64kbps (Media)', 'acodec': 'mp3', 'filesize': int(64 * 128 * duration_min) if duration else 0, 'filesize_mb': round(64 * 128 * duration_min / (1024 * 1024), 2) if duration else '~2-3'},
                    {'format_id': 'best', 'ext': 'mp3', 'abr': 128, 'abr_text': 'Mejor Disponible', 'acodec': 'mp3', 'filesize': int(128 * 128 * duration_min) if duration else 0, 'filesize_mb': round(128 * 128 * duration_min / (1024 * 1024), 2) if duration else '~4-6'},
                ]
            
            else:
                # Para otras plataformas, usar el método normal
                formats = []
                audio_formats = []
                seen_video = set()
                seen_audio = set()
                
                if 'formats' in info:
                    for f in info['formats']:
                        format_id = f.get('format_id')
                        ext = f.get('ext', 'unknown')
                        
                        # Formatos de video
                        if f.get('vcodec') != 'none' and f.get('height'):
                            filesize = f.get('filesize') or f.get('filesize_approx', 0)
                            quality_key = f'{f.get("height")}p-{f.get("fps", 0)}fps-{ext}'
                            
                            if quality_key not in seen_video:
                                seen_video.add(quality_key)
                                formats.append({
                                    'format_id': format_id,
                                    'ext': ext,
                                    'quality': f'{f.get("height")}p',
                                    'height': f.get('height', 0),
                                    'resolution': f'{f.get("width")}x{f.get("height")}',
                                    'fps': f.get('fps', 0),
                                    'vcodec': f.get('vcodec', 'unknown'),
                                    'acodec': f.get('acodec', 'none'),
                                    'filesize': filesize,
                                    'filesize_mb': round(filesize / (1024 * 1024), 2) if filesize else 'N/A',
                                    'has_audio': f.get('acodec') != 'none'
                                })
                        
                        # Formatos de audio
                        elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                            filesize = f.get('filesize') or f.get('filesize_approx', 0)
                            abr = f.get('abr', 0)
                            audio_key = f'{int(abr) if abr else 0}-{ext}'
                            
                            if audio_key not in seen_audio:
                                seen_audio.add(audio_key)
                                audio_formats.append({
                                    'format_id': format_id,
                                    'ext': ext,
                                    'abr': int(abr) if abr else 0,
                                    'abr_text': f'{int(abr)}kbps' if abr else 'N/A',
                                    'acodec': f.get('acodec', 'unknown'),
                                    'filesize': filesize,
                                    'filesize_mb': round(filesize / (1024 * 1024), 2) if filesize else 'N/A'
                                })
                
                # Si no se encontraron formatos específicos, usar "best" genérico
                if len(formats) == 0 and len(audio_formats) == 0:
                    print(f"[INFO] No se encontraron formatos específicos, usando configuración genérica 'best'")
                    # Determinar si el contenido es video o solo audio
                    has_video = info.get('vcodec') and info.get('vcodec') != 'none'
                    has_audio = info.get('acodec') and info.get('acodec') != 'none'
                    
                    # Calcular tamaño estimado basado en duración
                    duration_min = duration / 60 if duration else 5
                    
                    if has_video or not has_audio:  # Si tiene video o no está claro
                        # Ofrecer formatos de video genéricos
                        height = info.get('height', 720)
                        width = info.get('width', 1280)
                        ext = info.get('ext', 'mp4')
                        
                        formats.append({
                            'format_id': 'best',
                            'ext': ext,
                            'quality': 'Mejor Disponible',
                            'height': height,
                            'resolution': f'{width}x{height}' if width and height else 'Auto',
                            'fps': info.get('fps', 30),
                            'vcodec': info.get('vcodec', 'h264'),
                            'acodec': info.get('acodec', 'aac'),
                            'filesize': 0,
                            'filesize_mb': '~50-200',
                            'has_audio': True
                        })
                    
                    if has_audio:
                        # Ofrecer formatos de audio genéricos
                        audio_formats.append({
                            'format_id': 'bestaudio',
                            'ext': 'mp3',
                            'abr': info.get('abr', 128),
                            'abr_text': 'Mejor Disponible',
                            'acodec': info.get('acodec', 'mp3'),
                            'filesize': 0,
                            'filesize_mb': f'~{int(5 * duration_min)}-{int(10 * duration_min)}' if duration else '~5-15'
                        })
                
                # Ordenar formatos de menor a mayor calidad
                formats.sort(key=lambda x: (x['height'], x['fps']))
                audio_formats.sort(key=lambda x: x['abr'])
            
            # Obtener thumbnails disponibles
            thumbnails_list = []
            if 'thumbnails' in info and info['thumbnails']:
                for thumb in info['thumbnails']:
                    if thumb.get('url'):
                        thumbnails_list.append({
                            'url': thumb.get('url'),
                            'width': thumb.get('width', 0),
                            'height': thumb.get('height', 0),
                            'id': thumb.get('id', 'unknown')
                        })
            elif thumbnail:
                # Si no hay lista pero sí hay thumbnail principal
                thumbnails_list.append({
                    'url': thumbnail,
                    'width': 0,
                    'height': 0,
                    'id': 'default'
                })
            
            return jsonify({
                'title': title,
                'duration': duration,
                'thumbnail': thumbnail,
                'thumbnails': thumbnails_list,
                'formats': formats,
                'audio_formats': audio_formats
            })
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(f"[ERROR GET_FORMATS] DownloadError: {error_msg}")
        
        # Mensaje específico para detección de bot de YouTube
        if 'Sign in to confirm' in error_msg or 'not a bot' in error_msg or 'HTTP 429' in error_msg:
            return jsonify({
                'error': '⚠️ YouTube está bloqueando las descargas desde el servidor.\n\n'
                         '🔧 Esto sucede porque:\n'
                         '• Las cookies expiraron o están bloqueadas\n'
                         '• YouTube detectó demasiadas solicitudes\n\n'
                         '✅ Soluciones:\n'
                         '1. Espera 10-15 minutos e intenta de nuevo\n'
                         '2. Prueba con otro video de YouTube\n'
                         '3. Usa otras plataformas (TikTok, Instagram, etc.)\n\n'
                         '💡 Las cookies necesitan actualizarse periódicamente en el servidor.'
            }), 429
        
        # Mensaje específico para Spotify y otros servicios DRM
        if 'DRM' in error_msg or 'spotify' in url.lower():
            return jsonify({
                'error': 'Spotify usa protección DRM y no se puede descargar. 🎵\n\n'
                         'Alternativas:\n'
                         '• Busca la canción en YouTube y descárgala como MP3\n'
                         '• Usa SoundCloud (soundcloud.com)\n'
                         '• Usa Bandcamp para música independiente'
            }), 400
        
        return jsonify({'error': f'Error al obtener información del video: {error_msg}'}), 500
    except Exception as e:
        print(f"[ERROR GET_FORMATS] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    """Descarga el video/audio en el formato seleccionado"""
    try:
        data = request.get_json()
        url = data.get('url')
        format_id = data.get('format_id')
        download_type = data.get('type', 'video')  # 'video' o 'audio'
        output_format = data.get('output_format', 'mp4')  # Formato de salida deseado
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        # Generar ID único para esta descarga
        download_id = str(uuid.uuid4())
        
        # Detectar si es YouTube y usar Cobalt API
        is_youtube = 'youtube.com' in url or 'youtu.be' in url
        
        if is_youtube:
            print(f"[INFO] YouTube detectado - usando Cobalt API para descarga")
            
            try:
                if download_type == 'audio':
                    # Descargar solo audio con Cobalt
                    cobalt_url = download_with_cobalt_audio(url)
                    if not cobalt_url:
                        return jsonify({'error': 'No se pudo obtener el audio de YouTube. Intenta de nuevo.'}), 500
                    
                    # Descargar el archivo desde Cobalt
                    print(f"[COBALT] Descargando audio desde: {cobalt_url[:50]}...")
                    audio_response = requests.get(cobalt_url, stream=True, timeout=60)
                    
                    if audio_response.status_code != 200:
                        return jsonify({'error': f'Error al descargar audio: HTTP {audio_response.status_code}'}), 500
                    
                    # Guardar archivo
                    file_extension = output_format if output_format in ['mp3', 'wav', 'ogg'] else 'm4a'
                    output_filename = f"{download_id}.{file_extension}"
                    output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)
                    
                    with open(output_path, 'wb') as f:
                        for chunk in audio_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    print(f"[COBALT] ✓ Audio guardado: {output_filename}")
                    
                    return jsonify({
                        'success': True,
                        'download_id': download_id,
                        'filename': output_filename
                    })
                    
                else:
                    # Descargar video con Cobalt
                    # Mapear format_id a calidad de Cobalt
                    quality_map = {
                        'cobalt-max': 'max',
                        'cobalt-1440': '1440',
                        'cobalt-1080': '1080',
                        'cobalt-720': '720',
                        'cobalt-480': '480',
                        'cobalt-360': '360'
                    }
                    quality = quality_map.get(format_id, 'max')
                    
                    cobalt_url = download_with_cobalt(url, quality)
                    if not cobalt_url:
                        return jsonify({'error': f'No se pudo obtener el video en calidad {quality}. Intenta con otra calidad.'}), 500
                    
                    # Descargar el archivo desde Cobalt
                    print(f"[COBALT] Descargando video {quality} desde: {cobalt_url[:50]}...")
                    video_response = requests.get(cobalt_url, stream=True, timeout=120)
                    
                    if video_response.status_code != 200:
                        return jsonify({'error': f'Error al descargar video: HTTP {video_response.status_code}'}), 500
                    
                    # Guardar archivo
                    file_extension = output_format if output_format in ['mp4', 'webm', 'mkv'] else 'mp4'
                    output_filename = f"{download_id}.{file_extension}"
                    output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)
                    
                    total_size = int(video_response.headers.get('content-length', 0))
                    downloaded = 0
                    
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                # Actualizar progreso
                                if total_size > 0:
                                    download_progress[download_id] = {
                                        'status': 'downloading',
                                        'downloaded': downloaded,
                                        'total': total_size,
                                        'percentage': int((downloaded / total_size) * 100)
                                    }
                    
                    download_progress[download_id] = {'status': 'finished', 'filename': output_filename}
                    print(f"[COBALT] ✓ Video guardado: {output_filename}")
                    
                    return jsonify({
                        'success': True,
                        'download_id': download_id,
                        'filename': output_filename
                    })
                    
            except Exception as e:
                print(f"[ERROR COBALT] {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Error al descargar con Cobalt API: {str(e)}'}), 500
        
        # Para otras plataformas, usar yt-dlp como antes
        def progress_hook(d):
            if d['status'] == 'downloading':
                download_progress[download_id] = {
                    'status': 'downloading',
                    'downloaded': d.get('downloaded_bytes', 0),
                    'total': d.get('total_bytes') or d.get('total_bytes_estimate', 0),
                    'speed': d.get('speed', 0),
                    'eta': d.get('eta', 0)
                }
            elif d['status'] == 'finished':
                download_progress[download_id] = {
                    'status': 'finished',
                    'filename': d.get('filename', '')
                }
        
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{download_id}.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
            'no_check_certificate': True,
        }
        
        if download_type == 'audio':
            # Descargar solo audio - estrategia múltiple
            ydl_opts['format'] = 'bestaudio/best'
            
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': output_format,
                'preferredquality': '320' if output_format == 'mp3' else '0',
            }]
        else:
            # Descargar video - estrategia múltiple con fallbacks
            # Intenta: mejor video + mejor audio, si falla usa cualquier formato combinado
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            
            # Configurar formato de salida
            ydl_opts['merge_output_format'] = output_format if output_format else 'mp4'
        
        download_progress[download_id] = {'status': 'starting'}
        
        # Log para debug
        print(f"\n[DESCARGA] URL: {url}")
        print(f"[DESCARGA] Tipo: {download_type}")
        print(f"[DESCARGA] Format ID: {format_id}")
        print(f"[DESCARGA] Output format: {output_format}")
        print(f"[DESCARGA] Format string: {ydl_opts.get('format', 'N/A')}\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Buscar el archivo descargado
            downloaded_file = None
            for file in os.listdir(DOWNLOAD_FOLDER):
                if file.startswith(download_id):
                    downloaded_file = os.path.join(DOWNLOAD_FOLDER, file)
                    break
            
            if downloaded_file and os.path.exists(downloaded_file):
                filename = info.get('title', 'download')
                # Limpiar nombre de archivo
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
                ext = os.path.splitext(downloaded_file)[1]
                
                return jsonify({
                    'success': True,
                    'download_id': download_id,
                    'filename': f'{filename}{ext}',
                    'filepath': downloaded_file
                })
            else:
                return jsonify({'error': 'No se pudo encontrar el archivo descargado'}), 500
                
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        print(f"[ERROR] DownloadError: {error_msg}")
        
        # Mensajes de error más amigables
        if 'Requested format is not available' in error_msg:
            return jsonify({
                'error': 'El formato seleccionado no está disponible. Por favor, elige otra calidad o usa "Mejor calidad disponible".'
            }), 500
        elif '403' in error_msg or 'Forbidden' in error_msg:
            return jsonify({
                'error': 'Acceso bloqueado por YouTube. Las cookies pueden haber caducado. Exporta nuevas cookies desde tu navegador.'
            }), 500
        else:
            return jsonify({'error': f'Error al descargar: {error_msg}'}), 500
    except Exception as e:
        print(f"[ERROR] Exception: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_file/<download_id>')
def download_file(download_id):
    """Envía el archivo descargado al usuario"""
    try:
        # Buscar el archivo
        downloaded_file = None
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(download_id):
                downloaded_file = os.path.join(DOWNLOAD_FOLDER, file)
                break
        
        if downloaded_file and os.path.exists(downloaded_file):
            filename = request.args.get('filename', os.path.basename(downloaded_file))
            return send_file(
                downloaded_file,
                as_attachment=True,
                download_name=filename
            )
        else:
            return "Archivo no encontrado", 404
            
    except Exception as e:
        return str(e), 500

@app.route('/download_thumbnail', methods=['POST'])
def download_thumbnail():
    """Descarga y opcionalmente convierte una thumbnail"""
    try:
        import requests
        from PIL import Image
        from io import BytesIO
        
        data = request.get_json()
        thumbnail_url = data.get('url')
        output_format = data.get('format', 'jpg')
        index = data.get('index', 0)
        
        if not thumbnail_url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        # Descargar la imagen
        response = requests.get(thumbnail_url, timeout=30)
        response.raise_for_status()
        
        # Abrir la imagen
        img = Image.open(BytesIO(response.content))
        
        # Convertir si es necesario
        if img.mode in ('RGBA', 'LA', 'P') and output_format.lower() == 'jpg':
            # Convertir a RGB para JPG
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Guardar en memoria
        output = BytesIO()
        save_format = output_format.upper()
        if save_format == 'JPG':
            save_format = 'JPEG'
        
        img.save(output, format=save_format, quality=95)
        output.seek(0)
        
        # Determinar el tipo MIME
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'webp': 'image/webp'
        }
        mime_type = mime_types.get(output_format.lower(), 'image/jpeg')
        
        return send_file(
            output,
            mimetype=mime_type,
            as_attachment=True,
            download_name=f'thumbnail_{index + 1}.{output_format}'
        )
        
    except Exception as e:
        print(f"Error descargando thumbnail: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<download_id>')
def get_progress(download_id):
    """Obtiene el progreso de una descarga"""
    progress = download_progress.get(download_id, {'status': 'unknown'})
    return jsonify(progress)

@app.route('/cookies_status')
def cookies_status():
    """Verifica si hay cookies disponibles"""
    return jsonify({
        'has_cookies': os.path.exists(COOKIES_FILE) if COOKIES_FILE else False,
        'cookies_file': COOKIES_FILE
    })

@app.route('/get_trim_info', methods=['POST'])
def get_trim_info():
    """Obtiene información del video para calcular el tamaño estimado del recorte"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'Debe proporcionar una URL'}), 400
        
        # Obtener información del video
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        
        if COOKIES_FILE and os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        print(f"[TRIM INFO] Obteniendo información del video: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Obtener formatos disponibles
            formats = []
            if 'formats' in info:
                seen_qualities = set()
                for f in info['formats']:
                    if f.get('vcodec') != 'none' and f.get('height'):
                        height = f.get('height')
                        quality = f'{height}p'
                        
                        if quality not in seen_qualities:
                            seen_qualities.add(quality)
                            formats.append({
                                'quality': quality,
                                'quality_label': quality,  # Para mostrar en el selector
                                'height': height,
                                'format_id': f.get('format_id'),
                                'ext': f.get('ext', 'mp4'),
                                'filesize': f.get('filesize') or f.get('filesize_approx', 0),
                                'tbr': f.get('tbr', 0),  # Total bitrate
                            })
                
                # Ordenar por calidad (mayor a menor)
                formats.sort(key=lambda x: x['height'], reverse=True)
            
            duration = info.get('duration', 0)
            
            return jsonify({
                'success': True,
                'title': info.get('title', 'Video'),
                'duration': duration,
                'duration_formatted': f"{int(duration // 60)}:{int(duration % 60):02d}" if duration else "Desconocida",
                'formats': formats[:8],  # Limitar a las 8 mejores calidades
                'thumbnail': info.get('thumbnail', '')
            })
        
    except Exception as e:
        print(f"[ERROR TRIM INFO] {str(e)}")
        return jsonify({'error': f'Error al obtener información: {str(e)}'}), 500

@app.route('/trim_video', methods=['POST'])
def trim_video():
    """Recorta un video/audio desde un URL usando descarga directa con ffmpeg"""
    try:
        print("[TRIM] Iniciando proceso de recorte...", flush=True)
        data = request.get_json()
        print(f"[TRIM] Datos recibidos: {data}", flush=True)
        
        url = data.get('url')
        start_time = data.get('start_time', '00:00:00')  # Formato: HH:MM:SS
        end_time = data.get('end_time')
        quality = data.get('quality', 'best')  # Nueva: calidad seleccionada
        
        print(f"[TRIM] URL: {url}, Inicio: {start_time}, Fin: {end_time}, Calidad: {quality}", flush=True)
        
        if not url:
            print("[TRIM ERROR] No se proporcionó URL", flush=True)
            return jsonify({'error': 'Debe proporcionar una URL'}), 400
        
        if not end_time:
            print("[TRIM ERROR] No se especificó tiempo final", flush=True)
            return jsonify({'error': 'Debe especificar el tiempo final'}), 400
        
        # Generar ID único para la descarga
        download_id = str(uuid.uuid4())
        filename = f"trimmed_{download_id}.mp4"
        temp_file = os.path.join(DOWNLOAD_FOLDER, f"temp_{download_id}")
        output_file = os.path.join(DOWNLOAD_FOLDER, filename)
        
        # Construir selector de formato
        if quality and quality != 'best' and quality.endswith('p'):
            height = quality.replace('p', '')
            format_selector = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
        else:
            format_selector = 'bestvideo+bestaudio/best'
        
        print(f"[TRIM] Selector de formato: {format_selector}", flush=True)
        
        # Calcular duración del segmento
        def time_to_seconds(time_str):
            parts = time_str.split(':')
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)
        duration_seconds = end_seconds - start_seconds
        
        print(f"[TRIM] Segmento: {start_time} ({start_seconds}s) hasta {end_time} ({end_seconds}s) = {duration_seconds}s", flush=True)
        
        # MÉTODO SIMPLE: Descargar video completo y recortar
        print(f"[TRIM] Descargando video completo...", flush=True)
        
        ydl_opts = {
            'format': format_selector,
            'outtmpl': temp_file,
            'quiet': True,
            'no_warnings': True,
        }
        
        if COOKIES_FILE and os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print(f"[TRIM] Descarga completada, buscando archivo...", flush=True)
        
        # Buscar el archivo descargado (puede tener extensión diferente)
        downloaded_file = None
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(f"temp_{download_id}"):
                downloaded_file = os.path.join(DOWNLOAD_FOLDER, file)
                print(f"[TRIM] Archivo encontrado: {downloaded_file}", flush=True)
                break
        
        if not downloaded_file or not os.path.exists(downloaded_file):
            print(f"[TRIM ERROR] No se encontró el archivo descargado", flush=True)
            return jsonify({'error': 'Error al descargar el video'}), 500
        
        # Recortar con ffmpeg
        print(f"[TRIM] Recortando con ffmpeg...", flush=True)
        cmd = [
            'ffmpeg',
            '-ss', str(start_seconds),   # Seek ANTES de input (más rápido y preciso)
            '-i', downloaded_file,
            '-t', str(duration_seconds),
            '-c:v', 'copy',              # Copiar video sin re-encodear
            '-c:a', 'copy',              # Copiar audio sin re-encodear
            '-map', '0:v:0',             # Solo primer stream de video
            '-map', '0:a:0',             # Solo primer stream de audio
            '-map_metadata', '-1',       # Eliminar metadatos innecesarios
            '-fflags', '+genpts',        # Regenerar timestamps
            '-movflags', '+faststart',   # Optimizar para streaming
            '-y',
            output_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Eliminar archivo temporal
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)
            print(f"[TRIM] Archivo temporal eliminado", flush=True)
        
        if result.returncode != 0:
            print(f"[ERROR TRIM ffmpeg] {result.stderr}", flush=True)
            return jsonify({'error': f'Error al recortar: {result.stderr}'}), 500
        
        if not os.path.exists(output_file):
            print(f"[TRIM ERROR] El archivo recortado no se creó", flush=True)
            return jsonify({'error': 'Error al generar el archivo recortado'}), 500
        
        print(f"[TRIM] Proceso completado exitosamente: {output_file}", flush=True)
        
        # Obtener tamaño del archivo
        file_size = os.path.getsize(output_file)
        
        return jsonify({
            'success': True,
            'download_id': download_id,
            'filename': filename,
            'filesize': file_size,
            'filesize_mb': round(file_size / (1024 * 1024), 2)
        })
        
    except Exception as e:
        print(f"[ERROR TRIM] {str(e)}")
        return jsonify({'error': f'Error al recortar: {str(e)}'}), 500

@app.route('/download_trimmed/<download_id>')
def download_trimmed(download_id):
    """Descarga el archivo recortado"""
    try:
        # Buscar el archivo en la carpeta de descargas
        for filename in os.listdir(DOWNLOAD_FOLDER):
            if filename.startswith(f'trimmed_{download_id}'):
                filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                
                # Obtener el nombre limpio para la descarga
                ext = filename.split('.')[-1]
                download_name = f'recortado_{download_id}.{ext}'
                
                return send_file(
                    filepath,
                    as_attachment=True,
                    download_name=download_name
                )
        
        return jsonify({'error': 'Archivo no encontrado'}), 404
        
    except Exception as e:
        print(f"[ERROR DOWNLOAD] {str(e)}")
        return jsonify({'error': f'Error al descargar: {str(e)}'}), 500

@app.route('/trim_uploaded', methods=['POST'])
def trim_uploaded():
    """Recorta un archivo de video/audio subido por el usuario"""
    try:
        print("[TRIM UPLOAD] Iniciando proceso de recorte de archivo subido...", flush=True)
        
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó ningún archivo'}), 400
        
        file = request.files['file']
        start_time = request.form.get('start_time', '00:00:00')
        end_time = request.form.get('end_time')
        
        if not end_time:
            return jsonify({'error': 'Debe especificar el tiempo final'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400
        
        # Verificar espacio en disco disponible
        import shutil
        disk_usage = shutil.disk_usage(DOWNLOAD_FOLDER)
        free_space_gb = disk_usage.free / (1024**3)
        
        # Estimar espacio necesario (archivo original + recortado)
        # Como no sabemos el tamaño exacto del archivo hasta guardarlo, 
        # verificamos después de guardar
        
        print(f"[TRIM UPLOAD] Archivo: {file.filename}", flush=True)
        print(f"[TRIM UPLOAD] Espacio libre en disco: {free_space_gb:.2f} GB", flush=True)
        print(f"[TRIM UPLOAD] Inicio: {start_time}, Fin: {end_time}", flush=True)
        
        if free_space_gb < 1:
            return jsonify({'error': f'Espacio insuficiente en disco. Solo quedan {free_space_gb:.2f} GB libres. Libera al menos 5 GB para procesar archivos grandes.'}), 507
        
        # Generar ID único
        download_id = str(uuid.uuid4())
        
        # Guardar archivo subido temporalmente
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'mp4'
        temp_input = os.path.join(DOWNLOAD_FOLDER, f"upload_{download_id}.{file_ext}")
        
        print(f"[TRIM UPLOAD] Guardando archivo temporalmente...", flush=True)
        file.save(temp_input)
        
        # Verificar tamaño del archivo guardado
        file_size_gb = os.path.getsize(temp_input) / (1024**3)
        print(f"[TRIM UPLOAD] Archivo guardado: {temp_input} ({file_size_gb:.2f} GB)", flush=True)
        
        # Calcular duración del segmento
        def time_to_seconds(time_str):
            parts = time_str.split(':')
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)
        duration_seconds = end_seconds - start_seconds
        
        print(f"[TRIM UPLOAD] Recortando: {start_seconds}s a {end_seconds}s ({duration_seconds}s de duración)", flush=True)
        
        # Archivo de salida
        output_filename = f"trimmed_{download_id}.{file_ext}"
        output_file = os.path.join(DOWNLOAD_FOLDER, output_filename)
        
        # Recortar con ffmpeg usando método optimizado para archivos grandes
        # -ss ANTES de -i para buscar sin decodificar todo el archivo
        print(f"[TRIM UPLOAD] Ejecutando ffmpeg (método optimizado para archivos grandes)...", flush=True)
        cmd = [
            'ffmpeg',
            '-ss', str(start_seconds),  # Seek ANTES de input (más rápido)
            '-i', temp_input,
            '-t', str(duration_seconds),  # Duración a capturar
            '-c:v', 'copy',              # Copiar video sin re-encodear
            '-c:a', 'copy',              # Copiar audio sin re-encodear
            '-avoid_negative_ts', '1',   # Evitar timestamps negativos
            '-map', '0:v:0',             # Solo primer stream de video
            '-map', '0:a:0',             # Solo primer stream de audio
            '-map_metadata', '-1',       # Eliminar metadatos innecesarios
            '-fflags', '+genpts',        # Regenerar timestamps
            '-movflags', '+faststart',   # Optimizar para streaming
            '-y',
            output_file
        ]
        
        # Ejecutar con timeout para archivos grandes
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)  # 5 minutos máximo
        
        # Eliminar archivo temporal
        if os.path.exists(temp_input):
            os.remove(temp_input)
            print(f"[TRIM UPLOAD] Archivo temporal eliminado", flush=True)
        
        if result.returncode != 0:
            print(f"[ERROR TRIM UPLOAD] {result.stderr}", flush=True)
            return jsonify({'error': f'Error al recortar: {result.stderr}'}), 500
        
        if not os.path.exists(output_file):
            print(f"[ERROR TRIM UPLOAD] El archivo recortado no se creó", flush=True)
            return jsonify({'error': 'Error al generar el archivo recortado'}), 500
        
        # Obtener tamaño del archivo
        file_size = os.path.getsize(output_file)
        
        print(f"[TRIM UPLOAD] Proceso completado exitosamente: {output_file} ({file_size} bytes)", flush=True)
        
        return jsonify({
            'success': True,
            'download_id': download_id,
            'filename': output_filename,
            'filesize': file_size,
            'filesize_mb': round(file_size / (1024 * 1024), 2)
        })
        
    except subprocess.TimeoutExpired:
        print(f"[ERROR TRIM UPLOAD] Timeout - el proceso tardó más de 5 minutos", flush=True)
        # Limpiar archivo temporal si existe
        try:
            if 'temp_input' in locals() and os.path.exists(temp_input):
                os.remove(temp_input)
        except:
            pass
        return jsonify({'error': 'El proceso tardó demasiado tiempo. Intenta con un segmento más corto o un archivo más pequeño.'}), 500
    except Exception as e:
        print(f"[ERROR TRIM UPLOAD] {str(e)}", flush=True)
        # Limpiar archivo temporal si existe
        try:
            if 'temp_input' in locals() and os.path.exists(temp_input):
                os.remove(temp_input)
        except:
            pass
        return jsonify({'error': f'Error al procesar el archivo: {str(e)}'}), 500
    except Exception as e:
        print(f"[ERROR] Error al enviar archivo recortado: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/convert_format', methods=['POST'])
def convert_format():
    """Convierte un archivo a otro formato"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó ningún archivo'}), 400
        
        file = request.files['file']
        output_format = request.form.get('output_format', '').lower()
        
        if not file or file.filename == '':
            return jsonify({'error': 'Archivo inválido'}), 400
        
        if not output_format:
            return jsonify({'error': 'Debe especificar un formato de salida'}), 400
        
        # Generar ID único
        download_id = str(int(time.time() * 1000))
        
        # Guardar archivo temporal
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'bin'
        temp_input = os.path.join(DOWNLOAD_FOLDER, f"temp_convert_{download_id}.{file_ext}")
        file.save(temp_input)
        
        file_size_gb = os.path.getsize(temp_input) / (1024**3)
        print(f"[CONVERT] Archivo guardado: {temp_input} ({file_size_gb:.2f} GB)", flush=True)
        print(f"[CONVERT] Convirtiendo a formato: {output_format}", flush=True)
        
        # Archivo de salida
        output_filename = f"converted_{download_id}.{output_format}"
        output_file = os.path.join(DOWNLOAD_FOLDER, output_filename)
        
        # Configurar parámetros de ffmpeg según el formato
        cmd = ['ffmpeg', '-i', temp_input]
        
        # Configuración específica por formato
        if output_format in ['mp3', 'aac', 'ogg', 'm4a']:
            # Formatos de audio con pérdida - alta calidad
            cmd.extend([
                '-vn',  # Sin video
                '-codec:a', 'libmp3lame' if output_format == 'mp3' else 'aac' if output_format in ['aac', 'm4a'] else 'libvorbis',
                '-b:a', '320k',  # Bitrate alto
                '-y',
                output_file
            ])
        elif output_format in ['wav', 'flac']:
            # Formatos sin pérdida
            cmd.extend([
                '-vn',  # Sin video
                '-codec:a', 'pcm_s16le' if output_format == 'wav' else 'flac',
                '-y',
                output_file
            ])
        elif output_format in ['mp4', 'mkv', 'avi', 'webm', 'mov']:
            # Formatos de video - mantener calidad
            cmd.extend([
                '-codec:v', 'libx264' if output_format in ['mp4', 'mkv', 'avi', 'mov'] else 'libvpx-vp9',
                '-crf', '18',  # Calidad alta (rango: 0-51, menor = mejor)
                '-preset', 'medium',
                '-codec:a', 'aac',
                '-b:a', '256k',
                '-y',
                output_file
            ])
        else:
            os.remove(temp_input)
            return jsonify({'error': f'Formato no soportado: {output_format}'}), 400
        
        print(f"[CONVERT] Ejecutando ffmpeg...", flush=True)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        # Eliminar archivo temporal
        if os.path.exists(temp_input):
            os.remove(temp_input)
            print(f"[CONVERT] Archivo temporal eliminado", flush=True)
        
        if result.returncode != 0:
            print(f"[ERROR CONVERT] {result.stderr}", flush=True)
            return jsonify({'error': f'Error al convertir: {result.stderr}'}), 500
        
        if not os.path.exists(output_file):
            return jsonify({'error': 'Error al generar el archivo convertido'}), 500
        
        file_size = os.path.getsize(output_file)
        print(f"[CONVERT] Conversión completada: {output_file} ({file_size / (1024**2):.2f} MB)", flush=True)
        
        return jsonify({
            'success': True,
            'download_id': download_id,
            'filename': output_filename,
            'filesize_mb': round(file_size / (1024 * 1024), 2)
        })
        
    except subprocess.TimeoutExpired:
        if os.path.exists(temp_input):
            os.remove(temp_input)
        return jsonify({'error': 'Tiempo de conversión agotado (10 minutos)'}), 408
    except Exception as e:
        print(f"[ERROR CONVERT] {str(e)}", flush=True)
        if 'temp_input' in locals() and os.path.exists(temp_input):
            os.remove(temp_input)
        return jsonify({'error': f'Error al convertir el archivo: {str(e)}'}), 500

@app.route('/download_converted/<download_id>')
def download_converted(download_id):
    """Descarga el archivo convertido"""
    try:
        for filename in os.listdir(DOWNLOAD_FOLDER):
            if filename.startswith(f"converted_{download_id}"):
                filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                return send_file(filepath, as_attachment=True, download_name=filename)
        
        return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Verificar si hay cookies disponibles
    if COOKIES_FILE and os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
        print("✓ Cookies de YouTube cargadas desde:", COOKIES_FILE)
    else:
        print("⚠ No se encontraron cookies. Para evitar bloqueos de YouTube:")
        print("  Lee las instrucciones en COOKIES_SETUP.md")
    
    print("\n✓ Servidor iniciado en http://localhost:5000")
    print("Presiona Ctrl+C para detener el servidor\n")
    
    # Modo debug activado con threaded=True para mejor manejo de múltiples peticiones
    # use_reloader=True permite ver cambios en archivos sin reiniciar manualmente
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True, use_reloader=True)
