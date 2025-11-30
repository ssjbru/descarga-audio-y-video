from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import json
from pathlib import Path
import uuid
import threading
import time
import subprocess

app = Flask(__name__)

# Carpeta para descargas temporales
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
COOKIES_FILE = os.path.join(os.getcwd(), 'youtube_cookies.txt')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Diccionario para almacenar el progreso de las descargas
download_progress = {}

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
        if is_youtube:
            # Para YouTube, usar configuración sin cookies para obtener info
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_client': ['android_creator'],
                }
            }
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
        
        # Usar cookies si están disponibles
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE
            print(f"✓ Cookies de YouTube cargadas desde: {COOKIES_FILE}")
        else:
            print("⚠ No se encontraron cookies de YouTube")
        
        print(f"\n[INFO] Extrayendo información de: {url}")
        print(f"[INFO] Plataforma: {'YouTube' if is_youtube else 'SoundCloud' if is_soundcloud else 'Vimeo' if is_vimeo else 'Universal (yt-dlp auto-detect)'}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Obtener título
            title = info.get('title', 'Sin título')
            duration = info.get('duration', 0)
            thumbnail = info.get('thumbnail', '')
            
            # Para YouTube, usar calidades predefinidas en lugar de listar formatos específicos
            if is_youtube:
                # Obtener formatos reales para calcular tamaños aproximados
                real_formats = info.get('formats', [])
                size_map = {}
                
                # Mapear tamaños reales de los formatos disponibles
                for f in real_formats:
                    height = f.get('height', 0)
                    filesize = f.get('filesize') or f.get('filesize_approx', 0)
                    if height and filesize and height not in size_map:
                        size_map[height] = filesize
                
                formats = [
                    {'format_id': 'best[height<=144]', 'ext': 'mp4', 'quality': '144p', 'height': 144, 'resolution': '256x144', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(144, 0), 'filesize_mb': round(size_map.get(144, 0) / (1024 * 1024), 2) if size_map.get(144) else '~5-10', 'has_audio': True},
                    {'format_id': 'best[height<=240]', 'ext': 'mp4', 'quality': '240p', 'height': 240, 'resolution': '426x240', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(240, 0), 'filesize_mb': round(size_map.get(240, 0) / (1024 * 1024), 2) if size_map.get(240) else '~10-20', 'has_audio': True},
                    {'format_id': 'best[height<=360]', 'ext': 'mp4', 'quality': '360p', 'height': 360, 'resolution': '640x360', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(360, 0), 'filesize_mb': round(size_map.get(360, 0) / (1024 * 1024), 2) if size_map.get(360) else '~20-40', 'has_audio': True},
                    {'format_id': 'best[height<=480]', 'ext': 'mp4', 'quality': '480p', 'height': 480, 'resolution': '854x480', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(480, 0), 'filesize_mb': round(size_map.get(480, 0) / (1024 * 1024), 2) if size_map.get(480) else '~40-80', 'has_audio': True},
                    {'format_id': 'best[height<=720]', 'ext': 'mp4', 'quality': '720p', 'height': 720, 'resolution': '1280x720', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(720, 0), 'filesize_mb': round(size_map.get(720, 0) / (1024 * 1024), 2) if size_map.get(720) else '~80-150', 'has_audio': True},
                    {'format_id': 'best[height<=1080]', 'ext': 'mp4', 'quality': '1080p', 'height': 1080, 'resolution': '1920x1080', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(1080, 0), 'filesize_mb': round(size_map.get(1080, 0) / (1024 * 1024), 2) if size_map.get(1080) else '~150-300', 'has_audio': True},
                    {'format_id': 'best[height<=1440]', 'ext': 'mp4', 'quality': '1440p', 'height': 1440, 'resolution': '2560x1440', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(1440, 0), 'filesize_mb': round(size_map.get(1440, 0) / (1024 * 1024), 2) if size_map.get(1440) else '~300-500', 'has_audio': True},
                    {'format_id': 'best[height<=2160]', 'ext': 'mp4', 'quality': '4K', 'height': 2160, 'resolution': '3840x2160', 'fps': 30, 'vcodec': 'h264', 'acodec': 'aac', 'filesize': size_map.get(2160, 0), 'filesize_mb': round(size_map.get(2160, 0) / (1024 * 1024), 2) if size_map.get(2160) else '~500-1000', 'has_audio': True},
                ]
                
                # Calcular tamaños aproximados para audio basado en duración
                duration_min = duration / 60 if duration else 5
                
                audio_formats = [
                    {'format_id': 'bestaudio[abr<=64]', 'ext': 'm4a', 'abr': 64, 'abr_text': '64kbps', 'acodec': 'aac', 'filesize': int(64 * 128 * duration_min) if duration else 0, 'filesize_mb': round(64 * 128 * duration_min / (1024 * 1024), 2) if duration else '~3-5'},
                    {'format_id': 'bestaudio[abr<=128]', 'ext': 'm4a', 'abr': 128, 'abr_text': '128kbps', 'acodec': 'aac', 'filesize': int(128 * 128 * duration_min) if duration else 0, 'filesize_mb': round(128 * 128 * duration_min / (1024 * 1024), 2) if duration else '~5-8'},
                    {'format_id': 'bestaudio', 'ext': 'm4a', 'abr': 160, 'abr_text': 'Mejor Calidad', 'acodec': 'opus', 'filesize': int(160 * 128 * duration_min) if duration else 0, 'filesize_mb': round(160 * 128 * duration_min / (1024 * 1024), 2) if duration else '~8-12'},
                ]
            
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
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_creator'],
                }
            },
        }
        
        # Usar cookies SOLO para descarga (no para extraer info)
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        if download_type == 'audio':
            # Descargar solo audio
            if format_id and format_id != 'best':
                ydl_opts['format'] = format_id
            else:
                ydl_opts['format'] = 'bestaudio/best'
            
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': output_format,
                'preferredquality': '320' if output_format == 'mp3' else '0',
            }]
        else:
            # Descargar video
            if format_id and format_id != 'best':
                # Para formatos predefinidos de YouTube (con restricción de altura)
                if 'height<=' in format_id or '[' in format_id:
                    ydl_opts['format'] = f'{format_id}/best'
                else:
                    # Para otros formatos específicos
                    ydl_opts['format'] = f'{format_id}+bestaudio/best'
            else:
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
        'has_cookies': os.path.exists(COOKIES_FILE),
        'cookies_file': COOKIES_FILE
    })

@app.route('/trim_video', methods=['POST'])
def trim_video():
    """Recorta un video/audio desde un URL o archivo subido"""
    try:
        data = request.get_json()
        url = data.get('url')
        start_time = data.get('start_time', '00:00:00')  # Formato: HH:MM:SS
        end_time = data.get('end_time')
        
        if not url and 'file' not in request.files:
            return jsonify({'error': 'Debe proporcionar una URL o un archivo'}), 400
        
        if not end_time:
            return jsonify({'error': 'Debe especificar el tiempo final'}), 400
        
        # Generar ID único para la descarga
        download_id = str(uuid.uuid4())
        filename = f"trimmed_{download_id}"
        
        # Configurar yt-dlp para descargar el video
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{filename}_original.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        # Descargar el video
        print(f"[TRIM] Descargando video: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            original_file = ydl.prepare_filename(info)
            ext = info.get('ext', 'mp4')
        
        if not os.path.exists(original_file):
            return jsonify({'error': 'Error al descargar el archivo'}), 500
        
        # Archivo de salida recortado
        output_file = os.path.join(DOWNLOAD_FOLDER, f'{filename}_trimmed.{ext}')
        
        # Usar ffmpeg para recortar
        # Calcular duración si se proporciona end_time
        if end_time:
            # Formato: ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:30 -c copy output.mp4
            cmd = [
                'ffmpeg',
                '-i', original_file,
                '-ss', start_time,
                '-to', end_time,
                '-c', 'copy',
                '-y',  # Sobrescribir sin preguntar
                output_file
            ]
        else:
            cmd = [
                'ffmpeg',
                '-i', original_file,
                '-ss', start_time,
                '-c', 'copy',
                '-y',
                output_file
            ]
        
        print(f"[TRIM] Recortando desde {start_time} hasta {end_time}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Eliminar archivo original
        if os.path.exists(original_file):
            os.remove(original_file)
        
        if result.returncode != 0:
            print(f"[ERROR TRIM] {result.stderr}")
            return jsonify({'error': f'Error al recortar: {result.stderr}'}), 500
        
        if not os.path.exists(output_file):
            return jsonify({'error': 'Error al generar el archivo recortado'}), 500
        
        # Obtener tamaño del archivo
        file_size = os.path.getsize(output_file)
        
        return jsonify({
            'success': True,
            'download_id': download_id,
            'filename': f'{filename}_trimmed.{ext}',
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
            if filename.startswith(f'trimmed_{download_id}') and '_trimmed' in filename:
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
        print(f"[ERROR] Error al enviar archivo recortado: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Verificar si hay cookies disponibles
    if os.path.exists(COOKIES_FILE):
        print("✓ Cookies de YouTube cargadas desde:", COOKIES_FILE)
    else:
        print("⚠ No se encontraron cookies. Para evitar bloqueos de YouTube:")
        print("  Lee las instrucciones en COOKIES_SETUP.md")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
