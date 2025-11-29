"""
Servidor Flask con HTTPS y configuración de seguridad mejorada
Para usar en producción con certificado SSL
"""
from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import json
from pathlib import Path
import uuid
import threading
import time
import subprocess
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Configuración de seguridad
app.config['SESSION_COOKIE_SECURE'] = True  # Solo cookies sobre HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Proteger contra XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Proteger contra CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora

# Si está detrás de un proxy (Nginx, Cloudflare, etc.)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Headers de seguridad
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https:; img-src 'self' data: https:; media-src 'self' https:;"
    return response

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

# Importar todas las rutas desde app.py
from app import *

if __name__ == '__main__':
    import ssl
    
    # Verificar si hay cookies disponibles
    if os.path.exists(COOKIES_FILE):
        print("✓ Cookies de YouTube cargadas desde:", COOKIES_FILE)
    else:
        print("⚠ No se encontraron cookies. Para evitar bloqueos de YouTube:")
        print("  Lee las instrucciones en COOKIES_SETUP.md")
    
    # Verificar si existen certificados SSL
    cert_file = 'ssl/cert.pem'
    key_file = 'ssl/key.pem'
    
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("\n✓ Certificados SSL encontrados")
        print("✓ Iniciando servidor HTTPS en https://0.0.0.0:5000")
        print("✓ También disponible en https://localhost:5000")
        
        # Crear contexto SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        
        # Ejecutar con HTTPS
        app.run(
            debug=False,  # En producción usar False
            host='0.0.0.0',
            port=5000,
            ssl_context=context
        )
    else:
        print("\n⚠ No se encontraron certificados SSL")
        print("Para generar certificados auto-firmados (desarrollo):")
        print("  python generate_ssl.py")
        print("\nPara producción, usa certificados de Let's Encrypt:")
        print("  certbot certonly --standalone -d tudominio.com")
        print("\nIniciando servidor HTTP normal...")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
