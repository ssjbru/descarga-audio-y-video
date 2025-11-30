let currentUrl = '';
let videoFormats = [];
let audioFormats = [];
let thumbnails = [];
let currentThumbnailUrl = '';

function showElement(id) {
    document.getElementById(id).classList.remove('hidden');
}

function hideElement(id) {
    document.getElementById(id).classList.add('hidden');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    showElement('error');
    setTimeout(() => hideElement('error'), 5000);
}

function switchTab(tab) {
    const tabs = document.querySelectorAll('.tab-btn');
    const videoFormatsDiv = document.getElementById('videoFormats');
    const audioFormatsDiv = document.getElementById('audioFormats');
    const trimSection = document.getElementById('trimSection');
    const thumbnailFormatsDiv = document.getElementById('thumbnailFormats');

    // Remover active de todos
    tabs.forEach(t => t.classList.remove('active'));
    
    // Ocultar todos
    hideElement('videoFormats');
    hideElement('audioFormats');
    hideElement('trimSection');
    hideElement('thumbnailFormats');

    if (tab === 'video') {
        tabs[0].classList.add('active');
        showElement('videoFormats');
    } else if (tab === 'audio') {
        tabs[1].classList.add('active');
        showElement('audioFormats');
    } else if (tab === 'trim') {
        tabs[2].classList.add('active');
        showElement('trimSection');
    } else if (tab === 'thumbnail') {
        tabs[3].classList.add('active');
        showElement('thumbnailFormats');
    }
}

async function getFormats() {
    const urlInput = document.getElementById('urlInput');
    const url = urlInput.value.trim();

    if (!url) {
        showError('Por favor, ingresa una URL válida');
        return;
    }

    currentUrl = url;
    hideElement('error');
    hideElement('videoInfo');
    showElement('loading');

    try {
        const response = await fetch('/get_formats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error al obtener formatos');
        }

        hideElement('loading');
        displayVideoInfo(data);

    } catch (error) {
        hideElement('loading');
        showError(error.message);
    }
}

function displayVideoInfo(data) {
    // Mostrar información del video
    document.getElementById('videoTitle').textContent = data.title;
    const thumbnailUrl = data.thumbnail || 'https://via.placeholder.com/200x150?text=No+Thumbnail';
    document.getElementById('thumbnail').src = thumbnailUrl;
    currentThumbnailUrl = thumbnailUrl;
    
    const duration = formatDuration(data.duration);
    document.getElementById('videoDuration').textContent = `Duración: ${duration}`;

    videoFormats = data.formats;
    audioFormats = data.audio_formats;
    
    // Obtener thumbnails disponibles
    thumbnails = data.thumbnails || [];
    if (thumbnails.length === 0 && thumbnailUrl && thumbnailUrl !== 'https://via.placeholder.com/200x150?text=No+Thumbnail') {
        // Si no hay lista de thumbnails pero sí hay una URL, usar esa
        thumbnails = [{
            url: thumbnailUrl,
            width: 0,
            height: 0,
            id: 'default'
        }];
    }

    // Detectar si es SoundCloud (solo audio)
    const isSoundCloud = videoFormats.length === 0 && audioFormats.length > 0;

    // Mostrar formatos de video
    const videoFormatsList = document.getElementById('videoFormatsList');
    videoFormatsList.innerHTML = '';

    if (videoFormats.length === 0) {
        if (isSoundCloud) {
            videoFormatsList.innerHTML = '<p style="color: var(--text-muted);">🎵 SoundCloud solo ofrece audio. Ve a la pestaña "Audio" para descargar.</p>';
        } else {
            videoFormatsList.innerHTML = '<p style="color: var(--text-muted);">No hay formatos de video disponibles</p>';
        }
    } else {
        // Agregar opción de mejor calidad disponible
        const bestQualityItem = document.createElement('div');
        bestQualityItem.className = 'format-item best-quality';
        bestQualityItem.innerHTML = `
            <div class="format-info">
                <div class="format-quality">⭐ Mejor Calidad Disponible</div>
                <div class="format-details">Descarga automáticamente la mejor calidad de video + audio disponible</div>
            </div>
        `;
        const bestBtn = document.createElement('button');
        bestBtn.className = 'download-btn';
        bestBtn.textContent = '⬇️ Descargar';
        bestBtn.onclick = () => downloadFile('best', 'video');
        bestQualityItem.appendChild(bestBtn);
        videoFormatsList.appendChild(bestQualityItem);
        
        videoFormats.forEach(format => {
            const formatItem = createFormatItem(format, 'video');
            videoFormatsList.appendChild(formatItem);
        });
    }

    // Mostrar formatos de audio
    const audioFormatsList = document.getElementById('audioFormatsList');
    audioFormatsList.innerHTML = '';

    if (audioFormats.length === 0) {
        audioFormatsList.innerHTML = '<p style="color: var(--text-muted);">No hay formatos de audio disponibles</p>';
    } else {
        // Agregar opción de mejor calidad disponible
        const bestAudioItem = document.createElement('div');
        bestAudioItem.className = 'format-item best-quality';
        bestAudioItem.innerHTML = `
            <div class="format-info">
                <div class="format-quality">⭐ Mejor Calidad Disponible</div>
                <div class="format-details">Descarga automáticamente el mejor audio disponible</div>
            </div>
        `;
        const bestBtn = document.createElement('button');
        bestBtn.className = 'download-btn';
        bestBtn.textContent = '⬇️ Descargar';
        bestBtn.onclick = () => downloadFile('best', 'audio');
        bestAudioItem.appendChild(bestBtn);
        audioFormatsList.appendChild(bestAudioItem);
        
        audioFormats.forEach(format => {
            const formatItem = createFormatItem(format, 'audio');
            audioFormatsList.appendChild(formatItem);
        });
    }

    // Mostrar thumbnails disponibles
    const thumbnailsList = document.getElementById('thumbnailsList');
    thumbnailsList.innerHTML = '';

    if (thumbnails.length === 0) {
        thumbnailsList.innerHTML = '<p style="color: var(--text-muted);">No hay portadas disponibles</p>';
    } else {
        // Ordenar thumbnails por tamaño (de menor a mayor)
        const sortedThumbnails = [...thumbnails].sort((a, b) => {
            const sizeA = (a.width || 0) * (a.height || 0);
            const sizeB = (b.width || 0) * (b.height || 0);
            return sizeA - sizeB;
        });

        sortedThumbnails.forEach((thumbnail, index) => {
            const thumbnailItem = createThumbnailItem(thumbnail, index);
            thumbnailsList.appendChild(thumbnailItem);
        });
    }

    showElement('videoInfo');
    
    // Si es SoundCloud, cambiar automáticamente a la pestaña de audio
    if (isSoundCloud) {
        switchTab('audio');
    }
}

function createFormatItem(format, type) {
    const div = document.createElement('div');
    div.className = 'format-item';

    const infoDiv = document.createElement('div');
    infoDiv.className = 'format-info';

    if (type === 'video') {
        const quality = document.createElement('div');
        quality.className = 'format-quality';
        quality.textContent = format.quality;
        
        if (format.has_audio) {
            const badge = document.createElement('span');
            badge.className = 'format-badge';
            badge.textContent = 'Con Audio';
            quality.appendChild(badge);
        }

        const details = document.createElement('div');
        details.className = 'format-details';
        
        // Formatear tamaño de archivo
        let sizeText = '';
        if (typeof format.filesize_mb === 'number') {
            sizeText = `${format.filesize_mb} MB`;
        } else if (typeof format.filesize_mb === 'string' && format.filesize_mb.startsWith('~')) {
            sizeText = `${format.filesize_mb} MB`;
        } else {
            sizeText = 'Tamaño variable';
        }
        
        details.innerHTML = `
            <span>${format.ext.toUpperCase()}</span> • 
            <span>${format.resolution}</span> • 
            <span>${format.fps}fps</span> • 
            <span style="color: var(--secondary-color); font-weight: 700;">📦 ${sizeText}</span><br>
            <span style="font-size: 0.85rem; opacity: 0.8;">Códec: ${format.vcodec}</span>
        `;

        infoDiv.appendChild(quality);
        infoDiv.appendChild(details);
    } else {
        const quality = document.createElement('div');
        quality.className = 'format-quality';
        quality.textContent = format.abr_text;

        const details = document.createElement('div');
        details.className = 'format-details';
        
        // Formatear tamaño de archivo
        let sizeText = '';
        if (typeof format.filesize_mb === 'number') {
            sizeText = `${format.filesize_mb} MB`;
        } else if (typeof format.filesize_mb === 'string' && format.filesize_mb.startsWith('~')) {
            sizeText = `${format.filesize_mb} MB`;
        } else {
            sizeText = 'Tamaño variable';
        }
        
        details.innerHTML = `
            <span>${format.ext.toUpperCase()}</span> • 
            <span>Códec: ${format.acodec}</span> • 
            <span style="color: var(--secondary-color); font-weight: 700;">📦 ${sizeText}</span>
        `;

        infoDiv.appendChild(quality);
        infoDiv.appendChild(details);
    }

    const downloadBtn = document.createElement('button');
    downloadBtn.className = 'download-btn';
    downloadBtn.textContent = '⬇️ Descargar';
    downloadBtn.onclick = () => downloadFile(format.format_id, type);

    div.appendChild(infoDiv);
    div.appendChild(downloadBtn);

    return div;
}

function createThumbnailItem(thumbnail, index) {
    const div = document.createElement('div');
    div.className = 'format-item thumbnail-item';

    const infoDiv = document.createElement('div');
    infoDiv.className = 'format-info';

    // Crear preview de la imagen
    const preview = document.createElement('div');
    preview.className = 'thumbnail-preview';
    preview.style.cssText = `
        width: 120px;
        height: 90px;
        background-image: url('${thumbnail.url}');
        background-size: cover;
        background-position: center;
        border-radius: 8px;
        border: 2px solid var(--border-color);
        margin-right: 15px;
        flex-shrink: 0;
    `;

    const textInfo = document.createElement('div');
    textInfo.style.flex = '1';

    const quality = document.createElement('div');
    quality.className = 'format-quality';
    
    if (thumbnail.width && thumbnail.height) {
        quality.textContent = `${thumbnail.width}x${thumbnail.height}`;
        
        // Añadir badge de calidad
        if (thumbnail.width >= 1920) {
            const badge = document.createElement('span');
            badge.className = 'format-badge';
            badge.textContent = 'Alta Calidad';
            quality.appendChild(badge);
        }
    } else {
        quality.textContent = 'Portada Original';
    }

    const details = document.createElement('div');
    details.className = 'format-details';
    
    // Calcular megapíxeles si hay dimensiones
    let mpText = '';
    if (thumbnail.width && thumbnail.height) {
        const megapixels = ((thumbnail.width * thumbnail.height) / 1000000).toFixed(1);
        mpText = ` • ${megapixels} MP`;
    }
    
    details.innerHTML = `
        <span>Resolución: ${thumbnail.width || '?'}x${thumbnail.height || '?'}</span>${mpText}<br>
        <span style="font-size: 0.85rem; opacity: 0.8;">Formato original del servidor</span>
    `;

    textInfo.appendChild(quality);
    textInfo.appendChild(details);

    infoDiv.appendChild(preview);
    infoDiv.appendChild(textInfo);

    const downloadBtn = document.createElement('button');
    downloadBtn.className = 'download-btn';
    downloadBtn.textContent = '⬇️ Descargar';
    downloadBtn.onclick = () => downloadThumbnail(thumbnail.url, index);

    div.appendChild(infoDiv);
    div.appendChild(downloadBtn);

    return div;
}

async function downloadThumbnail(thumbnailUrl, index) {
    try {
        const outputFormat = document.getElementById('thumbnailFormat').value;
        
        // Crear un enlace temporal para descargar
        const link = document.createElement('a');
        link.href = thumbnailUrl;
        link.download = `thumbnail_${index + 1}.${outputFormat}`;
        link.target = '_blank';
        
        // Si necesitamos conversión de formato, hacerlo en el servidor
        if (thumbnailUrl.includes('http')) {
            const response = await fetch('/download_thumbnail', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    url: thumbnailUrl,
                    format: outputFormat,
                    index: index
                })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                link.href = url;
                link.download = `thumbnail_${index + 1}.${outputFormat}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
                
                showError('✅ Portada descargada exitosamente');
            } else {
                throw new Error('Error al descargar la portada');
            }
        } else {
            // Descarga directa
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            showError('✅ Portada descargada exitosamente');
        }
        
    } catch (error) {
        showError('Error al descargar la portada: ' + error.message);
    }
}

async function downloadFile(formatId, type) {
    hideElement('error');
    hideElement('videoInfo');
    showElement('downloadProgress');

    try {
        // Obtener el formato de salida seleccionado
        const outputFormat = type === 'audio' 
            ? document.getElementById('audioOutputFormat').value
            : document.getElementById('videoOutputFormat').value;

        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: currentUrl,
                format_id: formatId,
                type: type,
                output_format: outputFormat
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error al descargar');
        }

        // Simular progreso (ya que la descarga real es en el servidor)
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            updateProgress(progress);
            
            if (progress >= 100) {
                clearInterval(interval);
                // Descargar el archivo
                window.location.href = `/download_file/${data.download_id}?filename=${encodeURIComponent(data.filename)}`;
                
                setTimeout(() => {
                    hideElement('downloadProgress');
                    showElement('videoInfo');
                    showError('✅ Descarga completada exitosamente');
                }, 1000);
            }
        }, 500);

    } catch (error) {
        hideElement('downloadProgress');
        showElement('videoInfo');
        showError(error.message);
    }
}

function updateProgress(percent) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    progressFill.style.width = percent + '%';
    progressText.textContent = Math.round(percent) + '%';
}

function formatDuration(seconds) {
    if (!seconds) return 'Desconocido';
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

// Permitir presionar Enter para buscar formatos
document.getElementById('urlInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        getFormats();
    }
});

// Variables para el modal de sitios
let allSites = [];

async function loadAllSupportedSites() {
    const modal = document.getElementById('sitesModal');
    const loading = document.getElementById('sitesLoading');
    const sitesList = document.getElementById('sitesList');
    
    // Mostrar modal
    modal.classList.remove('hidden');
    loading.classList.remove('hidden');
    sitesList.classList.add('hidden');
    
    try {
        const response = await fetch('/supported_sites');
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        allSites = data.sites;
        
        // Actualizar el contador en el botón
        document.getElementById('sitesCount').textContent = data.total;
        
        // Mostrar los sitios
        displaySites(allSites);
        
        loading.classList.add('hidden');
        sitesList.classList.remove('hidden');
        
    } catch (error) {
        console.error('Error cargando sitios:', error);
        loading.innerHTML = `<p style="color: var(--danger-color);">Error al cargar las plataformas: ${error.message}</p>`;
    }
}

function displaySites(sites) {
    const sitesList = document.getElementById('sitesList');
    sitesList.innerHTML = '';
    
    sites.forEach(site => {
        const siteItem = document.createElement('div');
        siteItem.className = 'site-item';
        siteItem.textContent = site.name;
        siteItem.dataset.name = site.name.toLowerCase();
        sitesList.appendChild(siteItem);
    });
    
    updateSearchResults(sites.length);
}

function filterSites() {
    const searchTerm = document.getElementById('siteSearch').value.toLowerCase();
    const siteItems = document.querySelectorAll('.site-item');
    let visibleCount = 0;
    
    siteItems.forEach(item => {
        const siteName = item.dataset.name;
        if (siteName.includes(searchTerm)) {
            item.classList.remove('hidden');
            visibleCount++;
        } else {
            item.classList.add('hidden');
        }
    });
    
    updateSearchResults(visibleCount);
}

function updateSearchResults(count) {
    const searchResults = document.getElementById('searchResults');
    searchResults.textContent = `Mostrando ${count} plataforma${count !== 1 ? 's' : ''}`;
}

function closeModal() {
    const modal = document.getElementById('sitesModal');
    modal.classList.add('hidden');
    document.getElementById('siteSearch').value = '';
}

// Cerrar modal al hacer click fuera del contenido
document.addEventListener('click', (e) => {
    const modal = document.getElementById('sitesModal');
    if (e.target === modal) {
        closeModal();
    }
});

// Cerrar modal con la tecla Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// ========== FUNCIONES DE RECORTE ==========

function setTrimExample(start, end) {
    document.getElementById('startTime').value = start;
    document.getElementById('endTime').value = end;
}

function validateTimeFormat(time) {
    const regex = /^([0-9]{2}):([0-9]{2}):([0-9]{2})$/;
    return regex.test(time);
}

async function trimVideo() {
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    const trimProgress = document.getElementById('trimProgress');
    const trimStatus = document.getElementById('trimStatus');

    if (!currentUrl) {
        showError('❌ Primero debes buscar un video');
        return;
    }

    if (!startTime || !endTime) {
        showError('❌ Debes especificar el tiempo de inicio y fin');
        return;
    }

    if (!validateTimeFormat(startTime) || !validateTimeFormat(endTime)) {
        showError('❌ Formato de tiempo inválido. Use HH:MM:SS (ejemplo: 00:01:30)');
        return;
    }

    // Convertir a segundos para comparar
    const startSeconds = timeToSeconds(startTime);
    const endSeconds = timeToSeconds(endTime);

    if (startSeconds >= endSeconds) {
        showError('❌ El tiempo de inicio debe ser menor que el tiempo final');
        return;
    }

    try {
        showElement('trimProgress');
        trimStatus.textContent = '⏳ Descargando video...';

        const response = await fetch('/trim_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: currentUrl,
                start_time: startTime,
                end_time: endTime
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al recortar el video');
        }

        const data = await response.json();
        
        if (data.success) {
            trimStatus.textContent = '✅ ¡Recortado exitoso! Descargando...';
            
            // Descargar el archivo
            const downloadUrl = `/download_trimmed/${data.download_id}`;
            window.location.href = downloadUrl;
            
            setTimeout(() => {
                hideElement('trimProgress');
                trimStatus.textContent = 'Procesando...';
            }, 2000);
        } else {
            throw new Error(data.error || 'Error desconocido');
        }

    } catch (error) {
        console.error('Error al recortar:', error);
        showError(`❌ Error: ${error.message}`);
        hideElement('trimProgress');
        trimStatus.textContent = 'Procesando...';
    }
}

function timeToSeconds(time) {
    const parts = time.split(':');
    return parseInt(parts[0]) * 3600 + parseInt(parts[1]) * 60 + parseInt(parts[2]);
}
