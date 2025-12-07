import os
import tempfile
import shutil

print("=" * 60)
print("DIAGNÓSTICO DE COOKIES PARA RENDER")
print("=" * 60)

# Simular rutas de Render
test_paths = [
    '/etc/secrets/youtube_cookies.txt',  # Render Secret Files
    os.path.join(os.getcwd(), 'youtube_cookies.txt'),  # Local
    'youtube_cookies.txt'  # Relativo
]

print("\n1. BUSCANDO ARCHIVOS DE COOKIES:")
print("-" * 60)
for path in test_paths:
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    print(f"  {path}")
    print(f"    Existe: {exists}")
    if exists:
        print(f"    Tamaño: {size} bytes")
        
        # Verificar si es escribible
        try:
            with open(path, 'a'):
                pass
            print(f"    Escribible: SÍ")
        except:
            print(f"    Escribible: NO (solo lectura)")
        
        # Intentar leer primeras líneas
        try:
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if first_line:
                    print(f"    Primera línea: {first_line[:50]}...")
                else:
                    print(f"    ⚠️ Archivo vacío")
        except Exception as e:
            print(f"    ⚠️ Error leyendo: {e}")
    print()

print("\n2. PROBANDO COPIA A UBICACIÓN TEMPORAL:")
print("-" * 60)
for path in test_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"Intentando copiar: {path}")
        try:
            temp_dir = tempfile.gettempdir()
            temp_cookies = os.path.join(temp_dir, 'youtube_cookies_temp.txt')
            shutil.copy2(path, temp_cookies)
            print(f"  ✓ Copia exitosa a: {temp_cookies}")
            print(f"  ✓ Tamaño: {os.path.getsize(temp_cookies)} bytes")
            
            # Verificar que es escribible
            with open(temp_cookies, 'a') as f:
                pass
            print(f"  ✓ Archivo escribible")
            
            # Limpiar
            os.remove(temp_cookies)
            print(f"  ✓ Limpieza exitosa")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        break
else:
    print("  ⚠️ No se encontró ningún archivo de cookies válido")

print("\n3. VERIFICANDO FORMATO DE COOKIES:")
print("-" * 60)
for path in test_paths:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"Analizando: {path}")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"  Total de líneas: {len(lines)}")
                
                # Contar líneas de cookies válidas (no comentarios ni vacías)
                cookie_lines = [l for l in lines if l.strip() and not l.startswith('#')]
                print(f"  Líneas de cookies: {len(cookie_lines)}")
                
                # Verificar que empiece con comentario Netscape
                if lines[0].startswith('# Netscape HTTP Cookie File'):
                    print(f"  ✓ Formato Netscape correcto")
                else:
                    print(f"  ⚠️ No parece ser formato Netscape")
                    print(f"     Primera línea: {lines[0][:50]}")
                
                # Verificar que hay cookies de youtube.com
                youtube_cookies = [l for l in cookie_lines if 'youtube.com' in l or '.google.com' in l]
                print(f"  Cookies de YouTube/Google: {len(youtube_cookies)}")
                
                if youtube_cookies:
                    print(f"  ✓ Cookies de YouTube encontradas")
                else:
                    print(f"  ⚠️ NO hay cookies de YouTube")
                    
        except Exception as e:
            print(f"  ✗ Error: {e}")
        break
else:
    print("  ⚠️ No se encontró ningún archivo de cookies")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
