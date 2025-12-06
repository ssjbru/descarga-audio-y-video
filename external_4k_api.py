"""
API externa para obtener formatos 4K de YouTube
Usa servicios especializados con infraestructura anti-bloqueo
"""

import requests

# Opciones de APIs gratuitas para 4K
EXTERNAL_APIS = {
    'rapidapi_ytstream': {
        'url': 'https://ytstream-download-youtube-videos.p.rapidapi.com/dl',
        'headers': {
            'X-RapidAPI-Key': 'TU_API_KEY_AQUI',  # Necesitas registrarte
            'X-RapidAPI-Host': 'ytstream-download-youtube-videos.p.rapidapi.com'
        }
    },
    'invidious': {
        'url': 'https://inv.riverside.rocks/api/v1/videos/{video_id}',
        'public': True  # No requiere API key
    }
}

def get_4k_formats_external(video_id):
    """
    Intenta obtener formatos 4K usando APIs externas
    
    Args:
        video_id: ID del video de YouTube
        
    Returns:
        dict: Formatos disponibles incluyendo 4K si existe
    """
    
    # Método 1: Invidious (gratis, sin API key)
    try:
        invidious_url = f"https://inv.riverside.rocks/api/v1/videos/{video_id}"
        response = requests.get(invidious_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            formats = []
            
            for fmt in data.get('formatStreams', []) + data.get('adaptiveFormats', []):
                height = fmt.get('size', '').split('x')[-1] if 'x' in fmt.get('size', '') else None
                if height:
                    formats.append({
                        'height': int(height),
                        'url': fmt.get('url'),
                        'quality': fmt.get('qualityLabel', ''),
                        'filesize': fmt.get('clen', 0),
                        'ext': fmt.get('container', 'mp4')
                    })
            
            print(f"[EXTERNAL_API] ✓ Invidious encontró {len(formats)} formatos")
            return formats
            
    except Exception as e:
        print(f"[EXTERNAL_API] ⚠ Invidious falló: {e}")
    
    # Método 2: Piped (alternativa gratis)
    try:
        piped_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
        response = requests.get(piped_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            formats = []
            
            for fmt in data.get('videoStreams', []):
                height = fmt.get('height')
                if height:
                    formats.append({
                        'height': height,
                        'url': fmt.get('url'),
                        'quality': fmt.get('quality', ''),
                        'filesize': fmt.get('contentLength', 0),
                        'ext': fmt.get('format', 'mp4').lower()
                    })
            
            print(f"[EXTERNAL_API] ✓ Piped encontró {len(formats)} formatos")
            return formats
            
    except Exception as e:
        print(f"[EXTERNAL_API] ⚠ Piped falló: {e}")
    
    print("[EXTERNAL_API] ❌ Todas las APIs externas fallaron")
    return []


def merge_with_external_formats(yt_dlp_formats, video_id):
    """
    Combina formatos de yt-dlp con formatos de APIs externas
    Si yt-dlp no encuentra 4K, intenta con APIs externas
    
    Args:
        yt_dlp_formats: Lista de formatos de yt-dlp
        video_id: ID del video
        
    Returns:
        list: Formatos combinados con prioridad a yt-dlp
    """
    
    # Detectar alturas de yt-dlp
    yt_dlp_heights = set()
    for fmt in yt_dlp_formats:
        height = fmt.get('height')
        if height:
            yt_dlp_heights.add(height)
    
    # Si ya hay 4K (2160) o 8K (4320), no buscar externamente
    if 2160 in yt_dlp_heights or 4320 in yt_dlp_heights:
        print("[EXTERNAL_API] ✓ yt-dlp ya encontró 4K/8K")
        return yt_dlp_formats
    
    # Si solo hay hasta 1080p, buscar 4K externamente
    if yt_dlp_heights and max(yt_dlp_heights) <= 1080:
        print("[EXTERNAL_API] ⚠ yt-dlp solo encontró hasta 1080p, buscando 4K externamente...")
        
        external_formats = get_4k_formats_external(video_id)
        
        # Filtrar solo formatos 4K (2160p) y superiores
        high_quality_formats = [f for f in external_formats if f.get('height', 0) >= 2160]
        
        if high_quality_formats:
            print(f"[EXTERNAL_API] ✅ Encontrados {len(high_quality_formats)} formatos 4K+ externos")
            
            # Normalizar formato externo al formato de yt-dlp
            normalized_formats = []
            for ext_fmt in high_quality_formats:
                normalized = {
                    'height': ext_fmt['height'],
                    'width': int(ext_fmt['height'] * 16 / 9),  # Asumir 16:9
                    'ext': ext_fmt.get('ext', 'mp4'),
                    'vcodec': 'h264',
                    'acodec': 'aac',
                    'filesize': ext_fmt.get('filesize', 0),
                    'filesize_approx': ext_fmt.get('filesize', 0),
                    'format_id': f"external_{ext_fmt['height']}p",
                    'quality_label': ext_fmt.get('quality', f"{ext_fmt['height']}p"),
                    'fps': 60 if ext_fmt['height'] >= 1440 else 30,
                    'source': 'external_api'  # Marcar como externo
                }
                normalized_formats.append(normalized)
            
            # Agregar formatos externos al inicio (mayor calidad primero)
            return normalized_formats + yt_dlp_formats
    
    return yt_dlp_formats
