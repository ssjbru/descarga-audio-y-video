let currentUrl = '';
let videoFormats = [];
let audioFormats = [];
let thumbnails = [];
let currentThumbnailUrl = '';
let trimFormats = [];
let videoDuration = 0;
let uploadedFile = null;
let uploadedFileDuration = 0;

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

function switchMainTab(tab) {
    const tabs = document.querySelectorAll('.main-tabs .tab-btn');
    const urlSection = document.getElementById('urlSection');
    const uploadSection = document.getElementById('uploadSection');
    const convertSection = document.getElementById('convertSection');

    tabs.forEach(t => t.classList.remove('active'));

    if (tab === 'url') {
        tabs[0].classList.add('active');
        showElement('urlSection');
        hideElement('uploadSection');
        hideElement('convertSection');
    } else if (tab === 'upload') {
        tabs[1].classList.add('active');
        hideElement('urlSection');
        showElement('uploadSection');
        hideElement('convertSection');
    } else if (tab === 'convert') {
        tabs[2].classList.add('active');
        hideElement('urlSection');
        hideElement('uploadSection');
        showElement('convertSection');
    }
}

// ==================== FILE CONVERSION ====================

let convertFile_selected = null;

function handleConvertFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    convertFile_selected = file;
    
    const fileName = document.getElementById('convertFileName');
    const fileSize = document.getElementById('convertFileSize');
    
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    const fileSizeGB = (file.size / (1024 * 1024 * 1024)).toFixed(2);
    
    fileName.textContent = `📄 ${file.name}`;
    
    if (file.size > 1024 * 1024 * 1024) {
        fileSize.textContent = `📦 Tamaño: ${fileSizeGB} GB`;
    } else {
        fileSize.textContent = `📦 Tamaño: ${fileSizeMB} MB`;
    }
    fileSize.style.color = '';
    
    showElement('convertFileInfo');
}

async function convertFile() {
    const outputFormat = document.getElementById('outputFormat').value;
    const convertProgress = document.getElementById('convertProgress');
    const convertStatus = document.getElementById('convertStatus');
    const progressBar = document.getElementById('convertProgressBar');
    const progressPercentage = document.getElementById('convertProgressPercentage');
    const convertDetails = document.getElementById('convertDetails');

    if (!convertFile_selected) {
        showError('❌ Primero debes seleccionar un archivo');
        return;
    }

    if (!outputFormat) {
        showError('❌ Debes seleccionar un formato de salida');
        return;
    }

    try {
        showElement('convertProgress');
        convertStatus.textContent = '⏳ Subiendo archivo...';
        
        let progress = 0;
        progressBar.style.width = '0%';
        progressPercentage.textContent = '0%';
        
        const fileSize = convertFile_selected.size;
        const isLargeFile = fileSize > 100 * 1024 * 1024;
        const progressSpeed = isLargeFile ? 400 : 200;
        
        const progressInterval = setInterval(() => {
            if (progress < 85) {
                progress += Math.random() * (isLargeFile ? 2 : 8);
                if (progress > 85) progress = 85;
                const roundedProgress = Math.round(progress);
                progressBar.style.width = roundedProgress + '%';
                progressPercentage.textContent = roundedProgress + '%';
                
                if (progress < 30) {
                    convertDetails.textContent = '📤 Subiendo archivo al servidor...';
                } else if (progress < 60) {
                    convertDetails.textContent = '🔄 Convirtiendo formato...';
                } else {
                    convertDetails.textContent = '⚡ Finalizando conversión...';
                }
            }
        }, progressSpeed);

        const formData = new FormData();
        formData.append('file', convertFile_selected);
        formData.append('output_format', outputFormat);

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 600000);

        const response = await fetch('/convert_format', {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);
        clearInterval(progressInterval);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al convertir el archivo');
        }

        const data = await response.json();
        
        if (data.success) {
            progressBar.style.width = '100%';
            progressPercentage.textContent = '100%';
            convertStatus.textContent = '✅ ¡Conversión exitosa! Iniciando descarga...';
            convertDetails.textContent = `📊 Tamaño: ${data.filesize_mb} MB`;
            
            const downloadUrl = `/download_converted/${data.download_id}`;
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            setTimeout(() => {
                hideElement('convertProgress');
            }, 3000);
        }
    } catch (error) {
        console.error('Error:', error);
        if (error.name === 'AbortError') {
            showError('❌ Tiempo de espera agotado. El archivo es muy grande o la conversión está tardando mucho.');
        } else {
            showError('❌ ' + error.message);
        }
        hideElement('convertProgress');
    }
}

// ==================== INITIALIZATION ====================

// Configurar drag & drop para el área de subida
document.addEventListener('DOMContentLoaded', function() {
    
    // Setup drag & drop for upload area
    const uploadArea = document.getElementById('uploadArea');
    
    if (uploadArea) {
        // Prevenir comportamiento por defecto del navegador
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Resaltar cuando se arrastra sobre el área
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.style.borderColor = 'var(--primary-color)';
                uploadArea.style.background = 'rgba(99, 102, 241, 0.1)';
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.style.borderColor = 'rgba(99, 102, 241, 0.3)';
                uploadArea.style.background = 'rgba(15, 23, 42, 0.4)';
            });
        });

        // Manejar el drop
        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const fileInput = document.getElementById('fileInput');
                // Usar DataTransfer para asignar archivos correctamente
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(files[0]);
                fileInput.files = dataTransfer.files;
                
                // Disparar el evento change manualmente
                handleFileSelect({ target: { files: dataTransfer.files } });
            }
        });
    }
    
    // Setup drag & drop for convert area
    const convertUploadArea = document.getElementById('convertUploadArea');
    
    if (convertUploadArea) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            convertUploadArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            convertUploadArea.addEventListener(eventName, () => {
                convertUploadArea.style.borderColor = 'var(--primary-color)';
                convertUploadArea.style.background = 'rgba(99, 102, 241, 0.1)';
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            convertUploadArea.addEventListener(eventName, () => {
                convertUploadArea.style.borderColor = 'rgba(99, 102, 241, 0.3)';
                convertUploadArea.style.background = 'rgba(15, 23, 42, 0.4)';
            });
        });

        convertUploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const convertFileInput = document.getElementById('convertFileInput');
                // Usar DataTransfer para asignar archivos correctamente
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(files[0]);
                convertFileInput.files = dataTransfer.files;
                
                // Disparar el evento change manualmente
                handleConvertFileSelect({ target: { files: dataTransfer.files } });
            }
        });
    }
});

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    uploadedFile = file;
    
    // Mostrar información del archivo
    const fileName = document.getElementById('uploadedFileName');
    const fileSize = document.getElementById('uploadedFileSize');
    const fileDuration = document.getElementById('uploadedFileDuration');

    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    const fileSizeGB = (file.size / (1024 * 1024 * 1024)).toFixed(2);
    
    fileName.textContent = `📄 ${file.name}`;
    
    if (file.size > 1024 * 1024 * 1024) {
        fileSize.textContent = `📦 Tamaño: ${fileSizeGB} GB`;
    } else {
        fileSize.textContent = `📦 Tamaño: ${fileSizeMB} MB`;
    }
    fileSize.style.color = ''; // Sin color especial
    
    // Obtener duración del video/audio
    const url = URL.createObjectURL(file);
    const mediaElement = document.createElement(file.type.startsWith('video/') ? 'video' : 'audio');
    
    mediaElement.addEventListener('loadedmetadata', () => {
        uploadedFileDuration = Math.floor(mediaElement.duration);
        const hours = Math.floor(uploadedFileDuration / 3600);
        const minutes = Math.floor((uploadedFileDuration % 3600) / 60);
        const seconds = uploadedFileDuration % 60;
        
        const durationStr = hours > 0 
            ? `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
            : `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        fileDuration.textContent = `⏱️ Duración: ${durationStr}`;
        
        // Establecer tiempo final por defecto al final del archivo
        const endTimeStr = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        document.getElementById('uploadEndTime').value = endTimeStr;
        
        // Calcular tamaño inicial
        calculateUploadTrimSize();
        
        URL.revokeObjectURL(url);
    });
    
    mediaElement.src = url;
    
    showElement('uploadedFileInfo');
}

function calculateUploadTrimSize() {
    if (!uploadedFile || !uploadedFileDuration) return;
    
    const startTime = document.getElementById('uploadStartTime').value;
    const endTime = document.getElementById('uploadEndTime').value;
    
    if (!startTime || !endTime || !validateTimeFormat(startTime) || !validateTimeFormat(endTime)) {
        hideElement('uploadTrimEstimate');
        return;
    }
    
    const startSeconds = timeToSeconds(startTime);
    const endSeconds = timeToSeconds(endTime);
    
    if (startSeconds >= endSeconds || endSeconds > uploadedFileDuration) {
        hideElement('uploadTrimEstimate');
        return;
    }
    
    const trimDuration = endSeconds - startSeconds;
    const fileSizeBytes = uploadedFile.size;
    
    // Calcular proporción del archivo
    const proportion = trimDuration / uploadedFileDuration;
    const estimatedSizeBytes = fileSizeBytes * proportion;
    
    // Formatear el tamaño
    let sizeText;
    if (estimatedSizeBytes > 1024 * 1024 * 1024) {
        sizeText = (estimatedSizeBytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
    } else if (estimatedSizeBytes > 1024 * 1024) {
        sizeText = (estimatedSizeBytes / (1024 * 1024)).toFixed(2) + ' MB';
    } else {
        sizeText = (estimatedSizeBytes / 1024).toFixed(2) + ' KB';
    }
    
    document.getElementById('uploadEstimatedSize').textContent = sizeText;
    showElement('uploadTrimEstimate');
}

async function trimUploadedFile() {
    const startTime = document.getElementById('uploadStartTime').value;
    const endTime = document.getElementById('uploadEndTime').value;
    const uploadProgress = document.getElementById('uploadTrimProgress');
    const uploadStatus = document.getElementById('uploadTrimStatus');
    const progressBar = document.getElementById('uploadProgressBar');
    const progressDetails = document.getElementById('uploadTrimDetails');

    if (!uploadedFile) {
        showError('❌ Primero debes seleccionar un archivo');
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

    const startSeconds = timeToSeconds(startTime);
    const endSeconds = timeToSeconds(endTime);

    if (startSeconds >= endSeconds) {
        showError('❌ El tiempo de inicio debe ser menor que el tiempo final');
        return;
    }

    if (endSeconds > uploadedFileDuration) {
        showError('❌ El tiempo final excede la duración del archivo');
        return;
    }

    try {
        showElement('uploadTrimProgress');
        uploadStatus.textContent = '⏳ Subiendo archivo...';
        
        // Simular progreso de subida
        let progress = 0;
        const progressPercentage = document.getElementById('uploadProgressPercentage');
        progressBar.style.width = '0%';
        progressPercentage.textContent = '0%';
        
        // Para archivos grandes, el progreso será más lento y realista
        const fileSize = uploadedFile.size;
        const isLargeFile = fileSize > 100 * 1024 * 1024; // > 100 MB
        const progressSpeed = isLargeFile ? 300 : 150; // Más lento para archivos grandes
        
        const progressInterval = setInterval(() => {
            if (progress < 85) {
                progress += Math.random() * (isLargeFile ? 3 : 10);
                if (progress > 85) progress = 85;
                const roundedProgress = Math.round(progress);
                progressBar.style.width = roundedProgress + '%';
                progressPercentage.textContent = roundedProgress + '%';
                
                if (progress < 30) {
                    progressDetails.textContent = '📤 Subiendo archivo al servidor...';
                } else if (progress < 60) {
                    progressDetails.textContent = '✂️ Procesando video...';
                } else {
                    progressDetails.textContent = '⚡ Recortando segmento (esto puede tardar varios minutos para archivos grandes)...';
                }
            }
        }, isLargeFile ? 800 : progressSpeed);

        const formData = new FormData();
        formData.append('file', uploadedFile);
        formData.append('start_time', startTime);
        formData.append('end_time', endTime);

        // Aumentar timeout para archivos grandes (10 minutos)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 600000); // 10 minutos

        const response = await fetch('/trim_uploaded', {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);
        clearInterval(progressInterval);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al recortar el archivo');
        }

        const data = await response.json();
        
        if (data.success) {
            const progressPercentage = document.getElementById('uploadProgressPercentage');
            progressBar.style.width = '100%';
            progressPercentage.textContent = '100%';
            uploadStatus.textContent = '✅ ¡Recortado exitoso! Iniciando descarga...';
            progressDetails.textContent = `📊 Tamaño: ${data.filesize_mb} MB`;
            
            // Descargar el archivo
            const downloadUrl = `/download_trimmed/${data.download_id}`;
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            setTimeout(() => {
                hideElement('uploadTrimProgress');
                uploadStatus.textContent = 'Procesando...';
                progressBar.style.width = '0%';
                progressBar.textContent = '0%';
                progressDetails.textContent = '';
            }, 3000);
        } else {
            throw new Error(data.error || 'Error desconocido');
        }

    } catch (error) {
        console.error('Error al recortar archivo:', error);
        
        let errorMessage = error.message;
        if (error.name === 'AbortError') {
            errorMessage = 'El proceso tardó demasiado tiempo (más de 10 minutos). Intenta con un archivo más pequeño o un segmento más corto.';
        }
        
        showError(`❌ Error: ${errorMessage}`);
        hideElement('uploadTrimProgress');
        uploadStatus.textContent = 'Procesando...';
        progressBar.style.width = '0%';
        progressDetails.textContent = '';
    }
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
        // Cargar información del video para el trim si hay URL
        if (currentUrl) {
            fetchTrimInfo();
        }
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
                
                // Activar confetti de celebración
                triggerConfetti();
                
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

async function fetchTrimInfo() {
    if (!currentUrl) return;

    try {
        const response = await fetch('/get_trim_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: currentUrl })
        });

        if (!response.ok) {
            throw new Error('Error al obtener información del video');
        }

        const data = await response.json();
        
        if (data.success) {
            // Guardar información
            trimFormats = data.formats;
            videoDuration = data.duration;

            // Mostrar información del video
            const videoInfoDiv = document.getElementById('trimVideoInfo');
            videoInfoDiv.innerHTML = `
                <div style="margin-bottom: 10px;">
                    <strong>📹 ${data.title}</strong>
                </div>
                <div style="font-size: 0.9em; color: #666;">
                    ⏱️ Duración: ${formatDuration(data.duration)}
                </div>
            `;
            showElement('trimVideoInfo');

            // Llenar selector de calidad
            const qualitySelect = document.getElementById('trimQuality');
            qualitySelect.innerHTML = '<option value="">Seleccionar calidad...</option>';
            
            data.formats.forEach(format => {
                const option = document.createElement('option');
                option.value = format.quality;  // Enviar la resolución (ej: "1080p")
                option.textContent = format.quality_label;
                option.dataset.filesize = format.filesize;
                qualitySelect.appendChild(option);
            });

            showElement('trimQualitySection');

            // Actualizar estimados cuando cambie la selección
            qualitySelect.addEventListener('change', updateTrimEstimates);
            
            // Actualizar estimados cuando cambien los tiempos
            document.getElementById('startTime').addEventListener('input', updateTrimEstimates);
            document.getElementById('endTime').addEventListener('input', updateTrimEstimates);

        } else {
            throw new Error(data.error || 'Error desconocido');
        }

    } catch (error) {
        console.error('Error al obtener info del video:', error);
        showError(`❌ Error: ${error.message}`);
    }
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function updateTrimEstimates() {
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    const qualitySelect = document.getElementById('trimQuality');
    const selectedOption = qualitySelect.selectedOptions[0];

    if (!startTime || !endTime || !selectedOption || !selectedOption.value) {
        hideElement('trimEstimate');
        return;
    }

    if (!validateTimeFormat(startTime) || !validateTimeFormat(endTime)) {
        return;
    }

    const startSeconds = timeToSeconds(startTime);
    const endSeconds = timeToSeconds(endTime);

    if (startSeconds >= endSeconds) {
        return;
    }

    const duration = endSeconds - startSeconds;
    const filesize = parseInt(selectedOption.dataset.filesize);

    if (!filesize || filesize === 0) {
        // Estimar basado en bitrate promedio
        const estimatedSize = duration * 500 * 1024; // ~500 KB/s promedio
        displayTrimEstimate(estimatedSize, duration);
    } else {
        // Calcular tamaño basado en proporción del video completo
        const proportion = duration / videoDuration;
        const estimatedSize = filesize * proportion;
        displayTrimEstimate(estimatedSize, duration);
    }
}

function displayTrimEstimate(sizeBytes, duration) {
    const estimateDiv = document.getElementById('trimEstimate');
    
    // Formatear tamaño
    let sizeStr;
    if (sizeBytes > 1024 * 1024 * 1024) {
        sizeStr = (sizeBytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
    } else if (sizeBytes > 1024 * 1024) {
        sizeStr = (sizeBytes / (1024 * 1024)).toFixed(2) + ' MB';
    } else {
        sizeStr = (sizeBytes / 1024).toFixed(2) + ' KB';
    }

    // Estimar tiempo de descarga (asumiendo 5 Mbps promedio)
    const downloadSpeedBps = 5 * 1024 * 1024 / 8; // 5 Mbps en bytes/s
    const downloadTimeSeconds = sizeBytes / downloadSpeedBps;
    
    let timeStr;
    if (downloadTimeSeconds > 60) {
        const minutes = Math.floor(downloadTimeSeconds / 60);
        const seconds = Math.floor(downloadTimeSeconds % 60);
        timeStr = `${minutes}m ${seconds}s`;
    } else {
        timeStr = `${Math.ceil(downloadTimeSeconds)}s`;
    }

    estimateDiv.innerHTML = `
        <div style="margin-bottom: 5px;">
            <strong>📦 Tamaño estimado:</strong> ${sizeStr}
        </div>
        <div>
            <strong>⏱️ Tiempo estimado de descarga:</strong> ${timeStr}
        </div>
        <div style="font-size: 0.8em; color: #888; margin-top: 5px;">
            * Estimación basada en conexión de 5 Mbps
        </div>
    `;
    
    showElement('trimEstimate');
}

async function trimVideo() {
    console.log('[TRIM] Función trimVideo() llamada');
    
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    const quality = document.getElementById('trimQuality').value;
    const trimProgress = document.getElementById('trimProgress');
    const trimStatus = document.getElementById('trimStatus');

    console.log('[TRIM] Valores:', {startTime, endTime, quality, currentUrl});

    if (!currentUrl) {
        console.log('[TRIM ERROR] No hay URL');
        showError('❌ Primero debes buscar un video');
        return;
    }

    if (!startTime || !endTime) {
        console.log('[TRIM ERROR] Faltan tiempos');
        showError('❌ Debes especificar el tiempo de inicio y fin');
        return;
    }

    if (!validateTimeFormat(startTime) || !validateTimeFormat(endTime)) {
        console.log('[TRIM ERROR] Formato inválido');
        showError('❌ Formato de tiempo inválido. Use HH:MM:SS (ejemplo: 00:01:30)');
        return;
    }

    // Convertir a segundos para comparar
    const startSeconds = timeToSeconds(startTime);
    const endSeconds = timeToSeconds(endTime);

    if (startSeconds >= endSeconds) {
        console.log('[TRIM ERROR] Tiempo inicio >= tiempo final');
        showError('❌ El tiempo de inicio debe ser menor que el tiempo final');
        return;
    }

    try {
        console.log('[TRIM] Mostrando progreso...');
        showElement('trimProgress');
        trimStatus.textContent = '⏳ Preparando descarga...';
        
        const progressBar = document.getElementById('trimProgressBar');
        const progressDetails = document.getElementById('trimDetails');
        
        // Simular progreso durante la descarga
        let progress = 0;
        progressBar.style.width = '0%';
        progressBar.textContent = '0%';
        
        const progressInterval = setInterval(() => {
            if (progress < 90) {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90;
                progressBar.style.width = Math.round(progress) + '%';
                progressBar.textContent = Math.round(progress) + '%';
                
                // Actualizar detalles según el progreso
                if (progress < 30) {
                    progressDetails.textContent = '📥 Descargando video completo...';
                } else if (progress < 70) {
                    progressDetails.textContent = '✂️ Recortando segmento...';
                } else {
                    progressDetails.textContent = '📦 Preparando archivo final...';
                }
            }
        }, 500);

        const requestBody = {
            url: currentUrl,
            start_time: startTime,
            end_time: endTime
        };

        // Agregar calidad si fue seleccionada
        if (quality) {
            requestBody.quality = quality;
        }

        console.log('[TRIM] Enviando petición al backend:', requestBody);

        const response = await fetch('/trim_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        clearInterval(progressInterval);

        console.log('[TRIM] Respuesta recibida:', response.status, response.statusText);

        if (!response.ok) {
            const error = await response.json();
            console.log('[TRIM ERROR] Error del servidor:', error);
            throw new Error(error.error || 'Error al recortar el video');
        }

        const data = await response.json();
        console.log('[TRIM] Datos recibidos:', data);
        
        if (data.success) {
            progressBar.style.width = '100%';
            progressBar.textContent = '100%';
            trimStatus.textContent = '✅ ¡Recortado exitoso! Iniciando descarga...';
            progressDetails.textContent = `📊 Tamaño: ${data.filesize_mb} MB`;
            
            // Crear elemento <a> temporal para descargar con progreso nativo del navegador
            const downloadUrl = `/download_trimmed/${data.download_id}`;
            console.log('[TRIM] Descargando desde:', downloadUrl);
            
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            
            setTimeout(() => {
                hideElement('trimProgress');
                trimStatus.textContent = 'Procesando...';
                progressBar.style.width = '0%';
                progressBar.textContent = '0%';
                progressDetails.textContent = '';
            }, 3000);
        } else {
            throw new Error(data.error || 'Error desconocido');
        }

    } catch (error) {
        console.error('[TRIM ERROR] Error completo:', error);
        showError(`❌ Error: ${error.message}`);
        hideElement('trimProgress');
        trimStatus.textContent = 'Procesando...';
        document.getElementById('trimProgressBar').style.width = '0%';
        document.getElementById('trimDetails').textContent = '';
    }
}

function timeToSeconds(time) {
    const parts = time.split(':');
    return parseInt(parts[0]) * 3600 + parseInt(parts[1]) * 60 + parseInt(parts[2]);
}

// ============================================
// 🎨 MEJORAS VISUALES AVANZADAS
// ============================================

// Partículas flotantes de fondo
class FloatingParticles {
    constructor() {
        this.canvas = document.getElementById('effectsCanvas');
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 50;
        this.colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'];
        
        this.resize();
        this.createParticles();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                radius: Math.random() * 3 + 1,
                color: this.colors[Math.floor(Math.random() * this.colors.length)],
                speedX: (Math.random() - 0.5) * 0.5,
                speedY: (Math.random() - 0.5) * 0.5,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            if (particle.x < 0 || particle.x > this.canvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.speedY *= -1;
            
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = particle.color;
            this.ctx.globalAlpha = particle.opacity;
            this.ctx.fill();
        });
        
        this.ctx.globalAlpha = 1;
        requestAnimationFrame(() => this.animate());
    }
}

// Confetti mejorado para descargas exitosas
function triggerConfetti() {
    const container = document.getElementById('confettiContainer');
    if (!container) return;
    
    const colors = ['#6366f1', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6'];
    const confettiCount = 100;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti-piece';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 0.3 + 's';
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        container.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 4000);
    }
    
    // Agregar sonido de éxito si está activado
    const successSound = document.getElementById('successSound');
    if (successSound && localStorage.getItem('soundEffects') !== 'false') {
        successSound.currentTime = 0;
        successSound.volume = 0.3;
        successSound.play().catch(() => {});
    }
}

// Efecto de onda cuando se carga un video
function createWaveEffect(element) {
    const wave = document.createElement('div');
    wave.className = 'wave-effect';
    element.appendChild(wave);
    
    setTimeout(() => wave.remove(), 600);
}

// Animación de entrada suave para elementos
function animateIn(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        element.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 10);
}

// Loading spinner personalizado mejorado
function showModernLoading(message = 'Procesando...') {
    let loadingDiv = document.getElementById('modernLoading');
    if (!loadingDiv) {
        loadingDiv = document.createElement('div');
        loadingDiv.id = 'modernLoading';
        loadingDiv.className = 'modern-loading-overlay';
        loadingDiv.innerHTML = `
            <div class="modern-loading-content">
                <div class="loading-spinner-modern">
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                    <div class="spinner-ring"></div>
                </div>
                <p class="loading-text-modern">${message}</p>
                <div class="loading-progress-bar">
                    <div class="loading-progress-fill"></div>
                </div>
            </div>
        `;
        document.body.appendChild(loadingDiv);
    } else {
        loadingDiv.querySelector('.loading-text-modern').textContent = message;
        loadingDiv.style.display = 'flex';
    }
    
    // Animar barra de progreso
    const progressBar = loadingDiv.querySelector('.loading-progress-fill');
    progressBar.style.width = '0%';
    setTimeout(() => progressBar.style.width = '90%', 100);
}

function hideModernLoading() {
    const loadingDiv = document.getElementById('modernLoading');
    if (loadingDiv) {
        const progressBar = loadingDiv.querySelector('.loading-progress-fill');
        progressBar.style.width = '100%';
        setTimeout(() => {
            loadingDiv.style.display = 'none';
        }, 300);
    }
}

// Inicializar efectos al cargar
document.addEventListener('DOMContentLoaded', () => {
    // Iniciar partículas flotantes
    new FloatingParticles();
    
    // Animar elementos existentes
    document.querySelectorAll('.card, .info-card, .format-option').forEach((el, index) => {
        setTimeout(() => animateIn(el), index * 50);
    });
    
    // Agregar efectos de onda a botones principales
    document.querySelectorAll('.primary-btn, .search-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            createWaveEffect(this);
        });
    });
    
    console.log('✨ Mejoras visuales cargadas');
});
