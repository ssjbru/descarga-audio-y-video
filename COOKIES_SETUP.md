# 🍪 Configuración de Cookies para YouTube

Para evitar que YouTube detecte las descargas como bot, necesitas exportar tus cookies de navegador.

## Opción 1: Usar la Extensión "Get cookies.txt LOCALLY" (Recomendado)

### Para Chrome/Edge:
1. Instala la extensión: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

2. Ve a [YouTube.com](https://youtube.com) y **asegúrate de estar iniciado sesión**

3. Haz clic en el icono de la extensión

4. Haz clic en "Export" → Guarda el archivo como `youtube_cookies.txt`

5. Copia el archivo a la carpeta del proyecto:
   ```
   c:\Users\bruno\OneDrive\Documentos\descargardeyt\youtube_cookies.txt
   ```

### Para Firefox:
1. Instala: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Ve a YouTube.com (iniciado sesión)

3. Haz clic en el icono de la extensión → "Current Site"

4. Guarda como `youtube_cookies.txt` en la carpeta del proyecto

## Opción 2: Método Manual (Sin extensiones)

1. **Abre Chrome/Edge DevTools** (F12)

2. Ve a la pestaña **"Application"** (o "Aplicación")

3. En el menú izquierdo, ve a **"Cookies"** → selecciona `https://www.youtube.com`

4. Copia todas las cookies importantes (especialmente `CONSENT`, `VISITOR_INFO1_LIVE`, `LOGIN_INFO`)

5. Crea un archivo `youtube_cookies.txt` con este formato:
   ```
   # Netscape HTTP Cookie File
   .youtube.com	TRUE	/	TRUE	2147483647	CONSENT	YES+cb
   .youtube.com	TRUE	/	FALSE	1234567890	VISITOR_INFO1_LIVE	valor_aqui
   ```

## Verificar que las Cookies Funcionan

1. Reinicia el servidor (presiona Ctrl+C y ejecuta de nuevo `python app.py`)

2. Verifica en la consola que aparezca: "✓ Cookies de YouTube cargadas"

3. Intenta descargar un video de YouTube

## ⚠️ Notas Importantes

- **Las cookies caducan** - Si después de un tiempo vuelves a tener problemas, exporta las cookies nuevamente
- **Privacidad** - Las cookies contienen información de tu sesión. No las compartas
- El archivo `youtube_cookies.txt` debe estar en la misma carpeta que `app.py`
- Después de agregar las cookies, el servidor debe reiniciarse

## Solución de Problemas

### Sigue sin funcionar después de agregar cookies:
1. Asegúrate de que el archivo se llama exactamente `youtube_cookies.txt`
2. Verifica que esté en la carpeta correcta
3. Comprueba que iniciaste sesión en YouTube antes de exportar
4. Prueba cerrar sesión y volver a iniciar sesión en YouTube, luego exporta nuevamente

### El servidor no detecta las cookies:
- Reinicia el servidor completamente (Ctrl+C y volver a ejecutar)
- Verifica la ruta del archivo con el endpoint: http://localhost:5000/cookies_status
