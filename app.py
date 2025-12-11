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
import random
from external_4k_api import merge_with_external_formats

app = Flask(__name__)

# Configuración para permitir archivos grandes sin límite
app.config['MAX_CONTENT_LENGTH'] = None  # Sin límite de tamaño

# Configuración de cacheo para archivos estáticos
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # No cachear en desarrollo

# Carpeta para descargas temporales - Por defecto en disco local
# El usuario puede cambiarla desde la interfaz
DEFAULT_DOWNLOAD_FOLDER = os.path.join('C:\\', 'Temp', 'descargardepags')
DOWNLOAD_FOLDER = DEFAULT_DOWNLOAD_FOLDER

# Pool de User-Agents para rotar y evitar bloqueos
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
]

# Cache simple en memoria para metadatos de videos (TTL: 1 hora)
video_metadata_cache = {}
CACHE_TTL = 3600  # 1 hora en segundos

def get_random_user_agent():
    """Retorna un User-Agent aleatorio del pool"""
    return random.choice(USER_AGENTS)

def get_cached_metadata(video_id):
    """Obtiene metadata cacheada si existe y no ha expirado"""
    if video_id in video_metadata_cache:
        cached_data, timestamp = video_metadata_cache[video_id]
        if time.time() - timestamp < CACHE_TTL:
            print(f"[CACHE] ✓ Metadata encontrada para {video_id}")
            return cached_data
        else:
            print(f"[CACHE] ⏰ Metadata expirada para {video_id}")
            del video_metadata_cache[video_id]
    return None

def cache_metadata(video_id, metadata):
    """Guarda metadata en cache con timestamp"""
    video_metadata_cache[video_id] = (metadata, time.time())
    print(f"[CACHE] ✓ Metadata guardada para {video_id}")

# Buscar cookies en múltiples ubicaciones y manejar read-only
COOKIES_FILE = None
KICK_COOKIES_FILE = None
TWITCH_COOKIES_FILE = None

# Cookies de YouTube
possible_cookie_paths = [
    '/etc/secrets/youtube_cookies.txt',  # Render Secret Files
    '/etc/secrets/www.youtube.com_cookies',  # Render Secret Files (alternativo)
    os.path.join(os.getcwd(), 'youtube_cookies.txt'),  # Carpeta actual
    os.path.join(os.getcwd(), 'www.youtube.com_cookies'),  # Carpeta actual (alternativo)
]

for path in possible_cookie_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        # Copiar siempre a ubicación temporal escribible para evitar errores
        try:
            temp_dir = tempfile.gettempdir()
            temp_cookies = os.path.join(temp_dir, 'yt_cookies_writable.txt')
            shutil.copy2(path, temp_cookies)
            COOKIES_FILE = temp_cookies
            print(f"✓ Cookies de YouTube encontradas en: {path}")
            print(f"  → Copiadas a ubicación escribible: {temp_cookies}")
            break
        except Exception as e:
            print(f"⚠ Error copiando cookies de YouTube desde {path}: {e}")
            continue

# Cookies de Kick.com
kick_cookie_paths = [
    '/etc/secrets/kick.com_cookies.txt',
    '/etc/secrets/kick.com_cookies',  # Sin extensión
    os.path.join(os.getcwd(), 'kick.com_cookies.txt'),
    os.path.join(os.getcwd(), 'kick.com_cookies'),
]

for path in kick_cookie_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            temp_dir = tempfile.gettempdir()
            temp_cookies = os.path.join(temp_dir, 'kick_cookies_writable.txt')
            shutil.copy2(path, temp_cookies)
            KICK_COOKIES_FILE = temp_cookies
            print(f"✓ Cookies de Kick encontradas en: {path}")
            print(f"  → Copiadas a ubicación escribible: {temp_cookies}")
            break
        except Exception as e:
            print(f"⚠ Error copiando cookies de Kick desde {path}: {e}")
            continue

# Cookies de Twitch
twitch_cookie_paths = [
    '/etc/secrets/www.twitch.tv_cookies.txt',
    '/etc/secrets/www.twitch.tv_cookies',  # Sin extensión
    os.path.join(os.getcwd(), 'www.twitch.tv_cookies.txt'),
    os.path.join(os.getcwd(), 'www.twitch.tv_cookies'),
]

for path in twitch_cookie_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            temp_dir = tempfile.gettempdir()
            temp_cookies = os.path.join(temp_dir, 'twitch_cookies_writable.txt')
            shutil.copy2(path, temp_cookies)
            TWITCH_COOKIES_FILE = temp_cookies
            print(f"✓ Cookies de Twitch encontradas en: {path}")
            print(f"  → Copiadas a ubicación escribible: {temp_cookies}")
            break
        except Exception as e:
            print(f"⚠ Error copiando cookies de Twitch desde {path}: {e}")
            continue

if not COOKIES_FILE:
    print("⚠ No se encontraron cookies de YouTube")
    print("  → Las descargas funcionarán sin cookies (puede haber limitaciones)")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Diccionario para almacenar el progreso de las descargas
download_progress = {}

# Configuración de Cobalt API v9
# Instancias públicas que NO requieren autenticación
COBALT_INSTANCES = [
    "https://cobalt-api.kwiatekmiki.com",
    "https://api.cobalt.tools",  # Requiere JWT pero lo dejamos como backup
]

def get_streamlink_info(url):
    """
    Verifica que Streamlink puede acceder al video
    Retorna dict con información básica y calidades estándar
    """
    try:
        print(f"[STREAMLINK] Verificando acceso a: {url}")
        
        import subprocess
        
        # Comando streamlink para listar streams disponibles (sin descargar)
        cmd = ['streamlink', url]
        
        print(f"[STREAMLINK] Ejecutando: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"[STREAMLINK] Error stdout: {result.stdout[:500]}")
            print(f"[STREAMLINK] Error stderr: {result.stderr[:500]}")
            return None
        
        # Parsear output para extraer streams disponibles
        output = result.stdout
        print(f"[STREAMLINK] Output: {output[:500]}")
        
        # Buscar líneas con calidades (formato: "Available streams: ...")
        streams = []
        if 'Available streams:' in output:
            # Extraer calidades de la línea
            for line in output.split('\n'):
                if 'Available streams:' in line:
                    # Típicamente: "Available streams: 160p, 360p, 480p, 720p, 1080p (best)"
                    parts = line.split('Available streams:')[1].strip()
                    streams = [s.strip().replace('(best)', '').replace('(worst)', '') for s in parts.split(',')]
                    break
        
        # Si no se detectaron streams, usar calidades estándar
        if not streams:
            print(f"[STREAMLINK] No se detectaron streams específicos, usando calidades estándar")
            streams = ['best', '1080p', '720p', '480p', '360p', 'worst']
        
        # Extraer título del output (algunas plataformas lo muestran)
        title = 'Video'
        author = 'Unknown'
        if '[' in output and ']' in output:
            # Formato típico: [plugin][info] Title: ...
            for line in output.split('\n'):
                if 'title' in line.lower():
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        title = parts[1].strip()
                        break
        
        video_info = {
            'title': title,
            'author': author,
            'streams': streams,
            'url': url
        }
        
        print(f"[STREAMLINK] ✓ Título: {video_info['title']}")
        print(f"[STREAMLINK] ✓ Calidades disponibles: {', '.join(video_info['streams'])}")
        
        return video_info
        
    except subprocess.TimeoutExpired:
        print(f"[STREAMLINK] Timeout al obtener información")
        return None
    except Exception as e:
        print(f"[STREAMLINK] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def download_with_cobalt(url, quality='max'):
    """
    Descarga videos usando Cobalt API v9 (para YouTube principalmente)
    Retorna la URL de descarga directa o None si falla
    """
    # Intentar con todas las instancias disponibles
    for endpoint in COBALT_INSTANCES:
        try:
            print(f"[COBALT v9] Intentando con endpoint: {endpoint}")
            print(f"[COBALT v9] URL del video: {url}")
            print(f"[COBALT v9] Calidad solicitada: {quality}")
            
            # Formato de la API v9 según documentación oficial
            payload = {
                "url": url,
                "videoQuality": quality,
                "filenameStyle": "basic",
                "downloadMode": "auto"
            }
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            print(f"[COBALT v9] Payload: {payload}")
            # POST a la raíz del endpoint
            response = requests.post(f"{endpoint}/", json=payload, headers=headers, timeout=30)
            
            print(f"[COBALT v9] Código de respuesta: {response.status_code}")
            print(f"[COBALT v9] Respuesta completa: {response.text[:500]}")
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                print(f"[COBALT v9] Estado: {status}")
                
                # La v9 retorna directamente la URL en diferentes campos
                if status == 'tunnel' or status == 'redirect':
                    download_url = data.get('url')
                    if download_url:
                        print(f"[COBALT v9] ✓ URL de descarga obtenida: {download_url[:100]}...")
                        return download_url
                elif status == 'picker':
                    # Múltiples opciones
                    picker = data.get('picker', [])
                    if picker and len(picker) > 0:
                        download_url = picker[0].get('url')
                        if download_url:
                            print(f"[COBALT v9] ✓ URL de descarga obtenida (picker): {download_url[:100]}...")
                            return download_url
                elif status == 'error':
                    error_text = data.get('text', 'Error desconocido')
                    print(f"[COBALT v9] ✗ Error: {error_text}")
                else:
                    # Intentar extraer URL directamente si no hay status claro
                    download_url = data.get('url') or data.get('download')
                    if download_url:
                        print(f"[COBALT v9] ✓ URL extraída: {download_url[:100]}...")
                        return download_url
                    print(f"[COBALT v9] ✗ Estado no reconocido: {status}")
                    print(f"[COBALT v9] Datos completos: {data}")
            else:
                print(f"[COBALT v9] ✗ Error HTTP {response.status_code}")
                print(f"[COBALT v9] Respuesta: {response.text[:200]}")
                
        except Exception as e:
            print(f"[COBALT v9] ✗ Error con {endpoint}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"[COBALT v9] ✗ Todos los endpoints fallaron")
    return None

def download_with_cobalt_audio(url):
    """
    Descarga solo audio usando Cobalt API v9
    """
    # Intentar con todas las instancias disponibles
    for endpoint in COBALT_INSTANCES:
        try:
            print(f"[COBALT v9] Descargando audio con endpoint: {endpoint}")
            
            # Formato de la API v9
            payload = {
                "url": url,
                "audioFormat": "best",     # Nuevo en v9
                "filenameStyle": "basic",
                "downloadMode": "audio"    # Especificar que es solo audio
            }
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            print(f"[COBALT v9] Payload audio: {payload}")
            # POST a la raíz del endpoint
            response = requests.post(f"{endpoint}/", json=payload, headers=headers, timeout=30)
            
            print(f"[COBALT v9] Código de respuesta audio: {response.status_code}")
            print(f"[COBALT v9] Respuesta audio: {response.text[:500]}")
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                print(f"[COBALT v9] Estado audio: {status}")
                
                if status in ['tunnel', 'redirect']:
                    download_url = data.get('url')
                    if download_url:
                        print(f"[COBALT v9] ✓ URL de audio obtenida: {download_url[:100]}...")
                        return download_url
                elif status == 'error':
                    error_text = data.get('text', 'Error desconocido')
                    print(f"[COBALT v9] ✗ Error: {error_text}")
                else:
                    # Intentar extraer URL directamente
                    download_url = data.get('url') or data.get('download')
                    if download_url:
                        print(f"[COBALT v9] ✓ URL de audio extraída: {download_url[:100]}...")
                        return download_url
            
        except Exception as e:
            print(f"[COBALT v9] ✗ Error descargando audio con {endpoint}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"[COBALT v9] ✗ No se pudo obtener audio de ningún endpoint")
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

@app.route('/validate_batch_urls', methods=['POST'])
def validate_batch_urls():
    """Valida múltiples URLs para descarga por lotes"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls or not isinstance(urls, list):
            return jsonify({'error': 'URLs no proporcionadas o formato inválido'}), 400
        
        if len(urls) > 10:
            return jsonify({'error': 'Máximo 10 URLs permitidas'}), 400
        
        results = []
        
        for url in urls:
            try:
                # Validar formato básico
                if not url.startswith(('http://', 'https://')):
                    results.append({
                        'url': url,
                        'valid': False,
                        'error': 'URL debe comenzar con http:// o https://'
                    })
                    continue
                
                # Intentar obtener información básica con yt-dlp
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True,
                    'skip_download': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    results.append({
                        'url': url,
                        'valid': True,
                        'title': info.get('title', 'Sin título'),
                        'platform': info.get('extractor_key', 'Desconocido'),
                        'duration': info.get('duration', 0)
                    })
                    
            except Exception as e:
                results.append({
                    'url': url,
                    'valid': False,
                    'error': str(e)
                })
        
        return jsonify({'results': results})
        
    except Exception as e:
        print(f"[ERROR] Error al validar batch URLs: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
        'cookies_writable_path': COOKIES_FILE,
        'cookies_exists': os.path.exists(COOKIES_FILE) if COOKIES_FILE else False,
        'cookies_writable_exists': os.path.exists(COOKIES_FILE) if COOKIES_FILE else False,
        'is_render': os.path.exists('/opt/render'),
    }
    
    # Si hay cookies, obtener info adicional
    if COOKIES_FILE and os.path.exists(COOKIES_FILE):
        try:
            info['cookies_size'] = os.path.getsize(COOKIES_FILE)
            with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
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
        is_kick = 'kick.com' in url
        
        # USAR STREAMLINK PARA KICK/TWITCH - evita bloqueos completamente
        if is_kick or 'twitch.tv' in url:
            platform = 'KICK' if is_kick else 'TWITCH'
            print(f"[INFO] {platform} detectado - usando Streamlink")
            try:
                video_info = get_streamlink_info(url)
                
                if not video_info:
                    return jsonify({'error': f'No se pudo obtener información del video de {platform}.'}), 500
                
                # Obtener calidades disponibles de Streamlink
                available_streams = video_info.get('streams', [])
                
                if not available_streams:
                    return jsonify({'error': 'No hay streams disponibles para este video.'}), 500
                
                # Mapear calidades comunes
                quality_map = {
                    'best': 1080,
                    '1080p60': 1080,
                    '1080p': 1080,
                    '720p60': 720,
                    '720p': 720,
                    '480p': 480,
                    '360p': 360,
                    'worst': 240
                }
                
                # Crear formatos basados en streams disponibles
                formats_with_sizes = []
                for stream_name in available_streams:
                    quality = quality_map.get(stream_name, 720)
                    
                    # Estimación de bitrate por calidad
                    bitrate_map = {
                        1080: 6,
                        720: 3,
                        480: 1.5,
                        360: 0.8,
                        240: 0.5
                    }
                    bitrate = bitrate_map.get(quality, 3)
                    
                    formats_with_sizes.append({
                        'quality': quality,
                        'quality_label': stream_name,
                        'format': 'mp4',
                        'vcodec': 'h264',
                        'acodec': 'aac',
                        'filesize': 0,  # Streamlink no proporciona tamaño hasta descarga
                        'filesize_mb': 'Variable',
                        'stream_name': stream_name
                    })
                
                audio_formats = [
                    {
                        'format_id': f'{platform.lower()}-audio',
                        'ext': 'm4a',
                        'abr': 128,
                        'abr_text': 'Mejor Calidad',
                        'acodec': 'aac',
                        'filesize': 0,
                        'filesize_mb': 'Variable',
                    }
                ]
                
                print(f"[{platform}] ✓ {len(formats_with_sizes)} calidades disponibles")
                print(f"[{platform}] ✓ Todo listo para: {video_info['title']}")
                
                return jsonify({
                    'title': video_info['title'],
                    'duration': 0,  # Streamlink no siempre proporciona duración
                    'thumbnail': '',
                    'formats': formats_with_sizes,
                    'audio_formats': audio_formats,
                    'platform': platform.lower(),
                    'channel': video_info['author']
                })
                
            except Exception as e:
                print(f"[ERROR {platform}] {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Error al procesar video de {platform}: {str(e)}'}), 500
        
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
                
                # Verificar cache primero
                cached_data = get_cached_metadata(video_id)
                if cached_data:
                    print(f"[COBALT] ✓ Usando datos cacheados")
                    return jsonify({
                        'title': title,
                        'duration': cached_data.get('duration', 0),
                        'thumbnail': f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
                        'formats': cached_data['formats'],
                        'audio_formats': cached_data['audio_formats'],
                        'platform': 'youtube-cobalt'
                    })
                
                # ESTRATEGIA OPCIÓN C: yt-dlp detecta + Cobalt descarga
                # Usar yt-dlp SOLO para detección, Cobalt para descargar
                print(f"[COBALT] Detectando calidades reales con yt-dlp...")
                duration = 0
                available_formats = {}
                
                try:
                    user_agent = get_random_user_agent()
                    
                    # Configuración simple y efectiva
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'skip_download': True,
                        'socket_timeout': 30,
                        'http_headers': {
                            'User-Agent': user_agent,
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-us,en;q=0.5',
                            'Sec-Fetch-Mode': 'navigate',
                        }
                    }
                    if COOKIES_FILE and os.path.exists(COOKIES_FILE):
                        ydl_opts['cookiefile'] = COOKIES_FILE
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        
                        # Obtener duración
                        duration = info.get('duration', 0)
                        if duration > 0:
                            mins = duration // 60
                            secs = duration % 60
                            print(f"[COBALT] ✓ Duración: {duration}s ({mins}:{secs:02d})")
                        
                        # Obtener formatos
                        yt_formats = info.get('formats', [])
                        print(f"[COBALT] Total formatos encontrados: {len(yt_formats)}")
                        
                        # Detectar alturas únicas
                        all_heights = set()
                        for fmt in yt_formats:
                            height = fmt.get('height')
                            vcodec = fmt.get('vcodec', 'none')
                            if height and vcodec != 'none':
                                all_heights.add(height)
                                # Guardar mejor formato por altura
                                filesize = fmt.get('filesize') or fmt.get('filesize_approx', 0)
                                if height not in available_formats or filesize > available_formats[height].get('filesize', 0):
                                    available_formats[height] = fmt
                        
                        print(f"[COBALT] ✓ Calidades detectadas por yt-dlp: {sorted(all_heights, reverse=True)}")
                        
                        # Si no detectó 4K, intentar con APIs externas
                        if all_heights and max(all_heights) < 2160:
                            print(f"[COBALT] 🔄 yt-dlp solo encontró hasta {max(all_heights)}p")
                            print(f"[COBALT] 💡 Nota: Cobalt API puede tener acceso a 4K aunque yt-dlp no lo detecte")
                            print(f"[COBALT] 💡 Agregando 4K y 2K como opciones (Cobalt intentará descargarlas)")
                            
                            # Agregar 4K y 2K como disponibles para que Cobalt lo intente
                            if 2160 not in available_formats:
                                available_formats[2160] = {'filesize': 0}
                            if 1440 not in available_formats:
                                available_formats[1440] = {'filesize': 0}
                        
                        resolutions = sorted(available_formats.keys(), reverse=True)
                        print(f"[COBALT] ✓ Calidades finales a mostrar: {resolutions}")
                
                except Exception as e:
                    print(f"[COBALT] ⚠ Error en yt-dlp: {e}")
                    print(f"[COBALT] ⚠ Mostrando calidades estándar (Cobalt decidirá disponibilidad)")
                    duration = 180
                    available_formats = {
                        2160: {'filesize': 0},
                        1440: {'filesize': 0},
                        1080: {'filesize': 0},
                        720: {'filesize': 0},
                        480: {'filesize': 0},
                        360: {'filesize': 0},
                    }
                
                thumbnail = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
                
                # Generar formatos a partir de los detectados
                formats_with_sizes = []
                
                # Bitrates típicos de YouTube para estimaciones
                bitrate_estimates = {
                    2160: {'video': 12.0, 'audio': 0.128},
                    1440: {'video': 8.0, 'audio': 0.128},
                    1080: {'video': 5.0, 'audio': 0.128},
                    720: {'video': 2.5, 'audio': 0.128},
                    480: {'video': 1.0, 'audio': 0.128},
                    360: {'video': 0.5, 'audio': 0.128},
                }
                
                # Mapeo de calidades
                quality_map = {
                    2160: {'format_id': 'max', 'quality': '4K (2160p)', 'resolution': '3840x2160', 'fps': 60},
                    1440: {'format_id': '1440', 'quality': '2K (1440p)', 'resolution': '2560x1440', 'fps': 60},
                    1080: {'format_id': '1080', 'quality': 'Full HD (1080p)', 'resolution': '1920x1080', 'fps': 60},
                    720: {'format_id': '720', 'quality': 'HD (720p)', 'resolution': '1280x720', 'fps': 30},
                    480: {'format_id': '480', 'quality': 'SD (480p)', 'resolution': '854x480', 'fps': 30},
                    360: {'format_id': '360', 'quality': 'Baja (360p)', 'resolution': '640x360', 'fps': 30},
                }
                
                # Generar solo formatos disponibles
                for height in sorted(available_formats.keys(), reverse=True):
                    if height not in quality_map:
                        continue
                    
                    quality_info = quality_map[height]
                    fmt = available_formats[height]
                    
                    # Intentar obtener tamaño real
                    filesize = fmt.get('filesize', 0) if isinstance(fmt, dict) else 0
                    if not filesize:
                        filesize = fmt.get('filesize_approx', 0) if isinstance(fmt, dict) else 0
                    
                    # Si no hay tamaño, estimar con bitrate
                    if filesize == 0 and duration > 0:
                        bitrates = bitrate_estimates.get(height, {'video': 1.0, 'audio': 0.128})
                        total_bitrate_mbps = bitrates['video'] + bitrates['audio']
                        filesize = int((total_bitrate_mbps * duration * 1000000) / 8)
                    
                    filesize_mb = round(filesize / (1024 * 1024), 2) if filesize > 0 else 'Variable'
                    
                    print(f"[COBALT] ✓ {quality_info['quality']}: ~{filesize_mb} MB")
                    
                    formats_with_sizes.append({
                        'format_id': quality_info['format_id'],
                        'ext': fmt.get('ext', 'mp4') if isinstance(fmt, dict) else 'mp4',
                        'quality': quality_info['quality'],
                        'height': height,
                        'resolution': quality_info['resolution'],
                        'fps': fmt.get('fps', quality_info['fps']) if isinstance(fmt, dict) else quality_info['fps'],
                        'vcodec': fmt.get('vcodec', 'h264') if isinstance(fmt, dict) else 'h264',
                        'acodec': fmt.get('acodec', 'aac') if isinstance(fmt, dict) else 'aac',
                        'filesize': filesize,
                        'filesize_mb': filesize_mb,
                        'has_audio': True
                    })
                
                print(f"[COBALT] ✓ {len(formats_with_sizes)} calidades disponibles")
                
                # Calcular tamaño de audio
                if duration > 0:
                    audio_bitrate_kbps = 128
                    audio_filesize = int((audio_bitrate_kbps * duration * 1000) / 8)
                    audio_filesize_mb = round(audio_filesize / (1024 * 1024), 2)
                    print(f"[COBALT] ✓ Audio: ~{audio_filesize_mb} MB")
                else:
                    audio_filesize = 0
                    audio_filesize_mb = 'Variable'
                
                audio_formats = [
                    {'format_id': 'cobalt-audio', 'ext': 'm4a', 'abr': 128, 'abr_text': 'Mejor Calidad', 'acodec': 'aac', 'filesize': audio_filesize, 'filesize_mb': audio_filesize_mb},
                ]
                
                # Guardar en cache
                cache_metadata(video_id, {
                    'duration': duration,
                    'formats': formats_with_sizes,
                    'audio_formats': audio_formats
                })
                
                print(f"[COBALT] ✓ Todo listo para: {title}")
                
                return jsonify({
                    'title': title,
                    'duration': duration,
                    'thumbnail': thumbnail,
                    'formats': formats_with_sizes,
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
        
        # Headers específicos para Kick.com (protección anti-bot agresiva)
        if is_kick:
            print("[KICK] Detectado - aplicando configuración anti-bloqueo")
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://kick.com/',
                'Origin': 'https://kick.com',
            }
            # Usar cookies de Kick si están disponibles
            if KICK_COOKIES_FILE and os.path.exists(KICK_COOKIES_FILE):
                ydl_opts['cookiefile'] = KICK_COOKIES_FILE
                print(f"[KICK] ✓ Usando cookies desde: {KICK_COOKIES_FILE}")
            else:
                print("[KICK] ⚠ Sin cookies - puede fallar (se necesita sesión autenticada)")
                # Intentar cookies del navegador en local
                if not os.path.exists('/opt/render'):
                    try:
                        ydl_opts['cookiesfrombrowser'] = ('chrome',)
                        print("[KICK] Intentando cookies del navegador Chrome...")
                    except:
                        pass
        
        # Detectar Twitch
        is_twitch = 'twitch.tv' in url
        if is_twitch:
            print("[TWITCH] Detectado - aplicando configuración anti-bloqueo")
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.twitch.tv/',
            }
            # Usar cookies de Twitch si están disponibles
            if TWITCH_COOKIES_FILE and os.path.exists(TWITCH_COOKIES_FILE):
                ydl_opts['cookiefile'] = TWITCH_COOKIES_FILE
                print(f"[TWITCH] ✓ Usando cookies desde: {TWITCH_COOKIES_FILE}")
            else:
                print("[TWITCH] ⚠ Sin cookies - funcionalidad limitada")
        
        # Optimizaciones específicas por plataforma
        if False:  # Ya no usamos yt-dlp para YouTube
            # Usar cliente web con cookies para evitar bloqueos de bot
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['web'],  # Solo web client con cookies
                }
            }
            
            # USAR cookies - son necesarias para evitar detección de bot
            if COOKIES_FILE and os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
                ydl_opts['cookiefile'] = COOKIES_FILE
                print(f"✓ Cookies de YouTube cargadas desde archivo: {COOKIES_FILE}")
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
        
        # Mensaje específico para Kick/Twitch si Streamlink falla
        if ('kick.com' in url.lower() or 'twitch.tv' in url.lower()) and 'streamlink' in error_msg.lower():
            return jsonify({
                'error': '❌ Error al procesar el video\n\n'
                         '⚠️ La plataforma puede tener restricciones o el video no está disponible.\n\n'
                         '💡 Verifica:\n'
                         '• Que el video sea público\n'
                         '• Que la URL esté completa y correcta\n'
                         '• Que el video no esté eliminado'
            }), 403
        
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
        quality = data.get('quality')  # Para Kick: 1080, 720, 480, 360
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        # Generar ID único para esta descarga
        download_id = str(uuid.uuid4())
        
        # Detectar plataforma
        is_youtube = 'youtube.com' in url or 'youtu.be' in url
        is_kick = 'kick.com' in url
        
        # MANEJO DE KICK/TWITCH CON STREAMLINK
        if is_kick or 'twitch.tv' in url:
            platform = 'KICK' if is_kick else 'TWITCH'
            print(f"[{platform}] Iniciando descarga con Streamlink")
            
            try:
                output_file = os.path.join(DOWNLOAD_FOLDER, f'{download_id}.mp4')
                
                # Determinar calidad (best por defecto o usar el stream_name si está disponible)
                stream_quality = format_id if format_id else (quality if quality else 'best')
                
                print(f"[{platform}] URL: {url}")
                print(f"[{platform}] Calidad: {stream_quality}")
                print(f"[{platform}] Guardando en: {output_file}")
                
                # Comando streamlink para descargar
                import subprocess
                streamlink_cmd = [
                    'streamlink',
                    url,
                    stream_quality,
                    '-o', output_file,
                    '--force'  # Sobrescribir si existe
                ]
                
                print(f"[{platform}] Ejecutando: {' '.join(streamlink_cmd)}")
                
                # Ejecutar streamlink
                process = subprocess.Popen(
                    streamlink_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                stdout, stderr = process.communicate(timeout=600)  # 10 minutos timeout
                
                if process.returncode != 0:
                    print(f"[{platform}] Error streamlink: {stderr[:500]}")
                    return jsonify({'error': f'Error al descargar video: {stderr[:200]}'}), 500
                
                if not os.path.exists(output_file):
                    return jsonify({'error': 'El archivo no se descargó correctamente'}), 500
                
                print(f"[{platform}] ✓ Descarga completada: {os.path.getsize(output_file)} bytes")
                
                # Registrar descarga
                download_progress[download_id] = {
                    'status': 'completed',
                    'filename': f'{download_id}.mp4',
                    'title': f'{platform} Video'
                }
                
                return jsonify({
                    'success': True,
                    'download_id': download_id,
                    'message': 'Descarga completada'
                })
                
            except Exception as e:
                print(f"[KICK DOWNLOAD ERROR] {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Error al descargar desde Kick: {str(e)}'}), 500
        
        if is_youtube:
            print(f"[INFO] YouTube detectado - usando Cobalt API para descarga")
            
            try:
                if download_type == 'audio':
                    # Descargar solo audio con Cobalt
                    cobalt_url = download_with_cobalt_audio(url)
                    if not cobalt_url:
                        # Si Cobalt falla, usar yt-dlp como respaldo
                        print(f"[INFO] Cobalt audio falló, usando yt-dlp...")
                        try:
                            # Configuración optimizada para audio
                            ydl_opts = {
                                'format': 'bestaudio/best',
                                'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{download_id}.%(ext)s'),
                                'quiet': False,
                                'no_warnings': False,
                                'extract_flat': False,
                                'socket_timeout': 30,
                                'retries': 3,
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': output_format if output_format in ['mp3', 'wav', 'ogg'] else 'm4a',
                                }],
                                'http_headers': {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                                },
                            }
                            
                            if COOKIES_FILE and os.path.exists(COOKIES_FILE):
                                print(f"[YT-DLP] Usando cookies desde: {COOKIES_FILE}")
                                ydl_opts['cookiefile'] = COOKIES_FILE
                            else:
                                print(f"[YT-DLP] Sin cookies, continuando sin ellas")
                            
                            print(f"[YT-DLP] Descargando audio...")
                            
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(url, download=True)
                                file_extension = output_format if output_format in ['mp3', 'wav', 'ogg'] else 'm4a'
                                output_filename = f"{download_id}.{file_extension}"
                                
                                print(f"[YT-DLP] ✓ Audio descargado: {output_filename}")
                                
                                return jsonify({
                                    'success': True,
                                    'download_id': download_id,
                                    'filename': output_filename
                                })
                        except Exception as e:
                            print(f"[ERROR] yt-dlp audio falló: {e}")
                            import traceback
                            traceback.print_exc()
                            return jsonify({'error': f'No se pudo descargar el audio. Error: {str(e)}'}), 500
                    
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
                    # Mapear format_id a calidad de Cobalt (acepta ambos formatos)
                    quality_map = {
                        'max': 'max',
                        'cobalt-max': 'max',
                        '2160': '2160',
                        'cobalt-2160': '2160',
                        '1440': '1440',
                        'cobalt-1440': '1440',
                        '1080': '1080',
                        'cobalt-1080': '1080',
                        '720': '720',
                        'cobalt-720': '720',
                        '480': '480',
                        'cobalt-480': '480',
                        '360': '360',
                        'cobalt-360': '360'
                    }
                    quality = quality_map.get(format_id, 'max')
                    
                    print(f"[COBALT] format_id recibido: {format_id} → calidad Cobalt: {quality}")
                    
                    cobalt_url = download_with_cobalt(url, quality)
                    if not cobalt_url:
                        # Si Cobalt falla, intentar con yt-dlp como respaldo
                        print(f"[INFO] Cobalt falló, intentando con yt-dlp...")
                        try:
                            # Configuración optimizada de yt-dlp para YouTube
                            ydl_opts = {
                                'format': f'bestvideo[height<={quality if quality != "max" else "2160"}]+bestaudio/best',
                                'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{download_id}.%(ext)s'),
                                'quiet': False,  # Mostrar logs para debug
                                'no_warnings': False,
                                'extract_flat': False,
                                'socket_timeout': 30,
                                'retries': 3,
                                'fragment_retries': 3,
                                'http_headers': {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                                },
                            }
                            
                            # Solo usar cookies si existen
                            if COOKIES_FILE and os.path.exists(COOKIES_FILE):
                                print(f"[YT-DLP] Usando cookies desde: {COOKIES_FILE}")
                                ydl_opts['cookiefile'] = COOKIES_FILE
                            else:
                                print(f"[YT-DLP] Sin cookies, continuando sin ellas")
                            
                            print(f"[YT-DLP] Descargando video con formato: {ydl_opts['format']}")
                            
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                info = ydl.extract_info(url, download=True)
                                output_filename = ydl.prepare_filename(info)
                                output_filename = os.path.basename(output_filename)
                                
                                print(f"[YT-DLP] ✓ Video descargado: {output_filename}")
                                
                                return jsonify({
                                    'success': True,
                                    'download_id': download_id,
                                    'filename': output_filename
                                })
                        except Exception as e:
                            print(f"[ERROR] yt-dlp falló: {e}")
                            import traceback
                            traceback.print_exc()
                            return jsonify({'error': f'No se pudo descargar el video. Error: {str(e)}'}), 500
                    
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

# Log de versión de Streamlink para diagnóstico en Render
try:
    version = subprocess.getoutput("streamlink --version")
    print(f"[DEBUG] Streamlink version: {version}")
except Exception as e:
    print(f"[DEBUG] Error obteniendo versión de Streamlink: {e}")

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
