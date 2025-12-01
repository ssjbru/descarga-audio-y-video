// Sistema de traducciones multi-idioma
const translations = {
    en: {
        page_title: "Trimvert - Universal Media Tool",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Download, trim and convert media from 1000+ platforms in the best quality",
        dark_mode: "Dark Mode",
        light_mode: "Light Mode",
        language_label: "Language",
        tab_url: "🔗 From URL",
        tab_trim: "✂️ Trim File",
        tab_convert: "🔄 Convert Format",
        url_placeholder: "🔗 Paste here the link to your favorite video or song...",
        search_btn: "🔍 Search",
        upload_area_title: "Click or drag a file here",
        upload_area_desc: "Accepts video and audio files",
        file_selected: "📄 Selected file:",
        file_size: "📦 Size:",
        file_duration: "⏱️ Duration:",
        time_start: "⏱️ Start Time:",
        time_end: "⏱️ End Time:",
        time_format: "Format: HH:MM:SS",
        estimated_size: "📊 Estimated trim size:",
        trim_download_btn: "✂️ Trim and Download",
        convert_to: "🔄 Convert to:",
        select_format: "-- Select a format --",
        audio_formats: "🎵 Audio",
        video_formats: "🎬 Video",
        convert_btn: "🔄 Convert File",
        processing: "Processing...",
        uploading: "⏳ Uploading file...",
        converting: "🔄 Converting format...",
        trimming: "✂️ Processing video...",
        error_no_file: "❌ First you must select a file",
        error_no_format: "❌ You must select an output format",
        error_no_times: "❌ You must specify start and end time",
        error_invalid_time: "❌ Invalid time format. Use HH:MM:SS (example: 00:01:30)",
        error_start_greater: "❌ Start time must be less than end time",
        error_exceeds_duration: "❌ End time exceeds file duration",
        success_converted: "✅ Conversion successful! Starting download...",
        success_trimmed: "✅ Trim successful! Starting download..."
    },
    es: {
        page_title: "Trimvert - Herramienta Universal de Medios",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Descarga, recorta y convierte medios de más de 1000 plataformas en la mejor calidad",
        dark_mode: "Modo Oscuro",
        light_mode: "Modo Claro",
        language_label: "Idioma",
        tab_url: "🔗 Desde URL",
        tab_trim: "✂️ Recortar Archivo",
        tab_convert: "🔄 Convertir Formato",
        url_placeholder: "🔗 Pega aquí el enlace de tu video o canción favorita...",
        search_btn: "🔍 Buscar",
        upload_area_title: "Haz clic o arrastra un archivo aquí",
        upload_area_desc: "Acepta archivos de video y audio",
        file_selected: "📄 Archivo seleccionado:",
        file_size: "📦 Tamaño:",
        file_duration: "⏱️ Duración:",
        time_start: "⏱️ Tiempo de Inicio:",
        time_end: "⏱️ Tiempo Final:",
        time_format: "Formato: HH:MM:SS",
        estimated_size: "📊 Tamaño aproximado del recorte:",
        trim_download_btn: "✂️ Recortar y Descargar",
        convert_to: "🔄 Convertir a:",
        select_format: "-- Selecciona un formato --",
        audio_formats: "🎵 Audio",
        video_formats: "🎬 Video",
        convert_btn: "🔄 Convertir Archivo",
        processing: "Procesando...",
        uploading: "⏳ Subiendo archivo...",
        converting: "🔄 Convirtiendo formato...",
        trimming: "✂️ Procesando video...",
        error_no_file: "❌ Primero debes seleccionar un archivo",
        error_no_format: "❌ Debes seleccionar un formato de salida",
        error_no_times: "❌ Debes especificar el tiempo de inicio y fin",
        error_invalid_time: "❌ Formato de tiempo inválido. Use HH:MM:SS (ejemplo: 00:01:30)",
        error_start_greater: "❌ El tiempo de inicio debe ser menor que el tiempo final",
        error_exceeds_duration: "❌ El tiempo final excede la duración del archivo",
        success_converted: "✅ ¡Conversión exitosa! Iniciando descarga...",
        success_trimmed: "✅ ¡Recortado exitoso! Iniciando descarga..."
    },
    fr: {
        page_title: "Trimvert - Outil Média Universel",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Téléchargez, découpez et convertissez des médias depuis plus de 1000 plateformes en haute qualité",
        dark_mode: "Mode Sombre",
        light_mode: "Mode Clair",
        language_label: "Langue",
        tab_url: "🔗 Depuis URL",
        tab_trim: "✂️ Découper Fichier",
        tab_convert: "🔄 Convertir Format",
        url_placeholder: "🔗 Collez ici le lien de votre vidéo ou chanson préférée...",
        search_btn: "🔍 Rechercher",
        upload_area_title: "Cliquez ou glissez un fichier ici",
        upload_area_desc: "Accepte les fichiers vidéo et audio",
        file_selected: "📄 Fichier sélectionné:",
        file_size: "📦 Taille:",
        file_duration: "⏱️ Durée:",
        time_start: "⏱️ Temps de Début:",
        time_end: "⏱️ Temps de Fin:",
        time_format: "Format: HH:MM:SS",
        estimated_size: "📊 Taille estimée du découpage:",
        trim_download_btn: "✂️ Découper et Télécharger",
        convert_to: "🔄 Convertir en:",
        select_format: "-- Sélectionnez un format --",
        audio_formats: "🎵 Audio",
        video_formats: "🎬 Vidéo",
        convert_btn: "🔄 Convertir Fichier",
        processing: "Traitement...",
        uploading: "⏳ Téléchargement du fichier...",
        converting: "🔄 Conversion du format...",
        trimming: "✂️ Traitement de la vidéo...",
        error_no_file: "❌ Vous devez d'abord sélectionner un fichier",
        error_no_format: "❌ Vous devez sélectionner un format de sortie",
        error_no_times: "❌ Vous devez spécifier l'heure de début et de fin",
        error_invalid_time: "❌ Format de temps invalide. Utilisez HH:MM:SS (exemple: 00:01:30)",
        error_start_greater: "❌ L'heure de début doit être inférieure à l'heure de fin",
        error_exceeds_duration: "❌ L'heure de fin dépasse la durée du fichier",
        success_converted: "✅ Conversion réussie! Démarrage du téléchargement...",
        success_trimmed: "✅ Découpage réussi! Démarrage du téléchargement..."
    },
    de: {
        page_title: "Trimvert - Universelles Medien-Tool",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Laden Sie Medien von über 1000 Plattformen herunter, schneiden und konvertieren Sie sie in bester Qualität",
        dark_mode: "Dunkler Modus",
        light_mode: "Heller Modus",
        language_label: "Sprache",
        tab_url: "🔗 Von URL",
        tab_trim: "✂️ Datei Schneiden",
        tab_convert: "🔄 Format Konvertieren",
        url_placeholder: "🔗 Fügen Sie hier den Link zu Ihrem Lieblingsvideo oder -song ein...",
        search_btn: "🔍 Suchen",
        upload_area_title: "Klicken oder ziehen Sie eine Datei hierher",
        upload_area_desc: "Akzeptiert Video- und Audiodateien",
        file_selected: "📄 Ausgewählte Datei:",
        file_size: "📦 Größe:",
        file_duration: "⏱️ Dauer:",
        time_start: "⏱️ Startzeit:",
        time_end: "⏱️ Endzeit:",
        time_format: "Format: HH:MM:SS",
        estimated_size: "📊 Geschätzte Schnittgröße:",
        trim_download_btn: "✂️ Schneiden und Herunterladen",
        convert_to: "🔄 Konvertieren zu:",
        select_format: "-- Format auswählen --",
        audio_formats: "🎵 Audio",
        video_formats: "🎬 Video",
        convert_btn: "🔄 Datei Konvertieren",
        processing: "Verarbeitung...",
        uploading: "⏳ Datei hochladen...",
        converting: "🔄 Format konvertieren...",
        trimming: "✂️ Video verarbeiten...",
        error_no_file: "❌ Sie müssen zuerst eine Datei auswählen",
        error_no_format: "❌ Sie müssen ein Ausgabeformat auswählen",
        error_no_times: "❌ Sie müssen Start- und Endzeit angeben",
        error_invalid_time: "❌ Ungültiges Zeitformat. Verwenden Sie HH:MM:SS (Beispiel: 00:01:30)",
        error_start_greater: "❌ Die Startzeit muss kleiner sein als die Endzeit",
        error_exceeds_duration: "❌ Die Endzeit überschreitet die Dateidauer",
        success_converted: "✅ Konvertierung erfolgreich! Download wird gestartet...",
        success_trimmed: "✅ Schnitt erfolgreich! Download wird gestartet..."
    },
    pt: {
        page_title: "Trimvert - Ferramenta Universal de Mídia",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Baixe, corte e converta mídia de mais de 1000 plataformas na melhor qualidade",
        dark_mode: "Modo Escuro",
        light_mode: "Modo Claro",
        language_label: "Idioma",
        tab_url: "🔗 De URL",
        tab_trim: "✂️ Cortar Arquivo",
        tab_convert: "🔄 Converter Formato",
        url_placeholder: "🔗 Cole aqui o link do seu vídeo ou música favorita...",
        search_btn: "🔍 Buscar",
        upload_area_title: "Clique ou arraste um arquivo aqui",
        upload_area_desc: "Aceita arquivos de vídeo e áudio",
        file_selected: "📄 Arquivo selecionado:",
        file_size: "📦 Tamanho:",
        file_duration: "⏱️ Duração:",
        time_start: "⏱️ Tempo Inicial:",
        time_end: "⏱️ Tempo Final:",
        time_format: "Formato: HH:MM:SS",
        estimated_size: "📊 Tamanho aproximado do corte:",
        trim_download_btn: "✂️ Cortar e Baixar",
        convert_to: "🔄 Converter para:",
        select_format: "-- Selecione um formato --",
        audio_formats: "🎵 Áudio",
        video_formats: "🎬 Vídeo",
        convert_btn: "🔄 Converter Arquivo",
        processing: "Processando...",
        uploading: "⏳ Enviando arquivo...",
        converting: "🔄 Convertendo formato...",
        trimming: "✂️ Processando vídeo...",
        error_no_file: "❌ Primeiro você deve selecionar um arquivo",
        error_no_format: "❌ Você deve selecionar um formato de saída",
        error_no_times: "❌ Você deve especificar o tempo inicial e final",
        error_invalid_time: "❌ Formato de tempo inválido. Use HH:MM:SS (exemplo: 00:01:30)",
        error_start_greater: "❌ O tempo inicial deve ser menor que o tempo final",
        error_exceeds_duration: "❌ O tempo final excede a duração do arquivo",
        success_converted: "✅ Conversão bem-sucedida! Iniciando download...",
        success_trimmed: "✅ Corte bem-sucedido! Iniciando download..."
    },
    it: {
        page_title: "Trimvert - Strumento Multimediale Universale",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Scarica, taglia e converti media da oltre 1000 piattaforme nella migliore qualità",
        dark_mode: "Modalità Scura",
        light_mode: "Modalità Chiara",
        language_label: "Lingua",
        tab_url: "🔗 Da URL",
        tab_trim: "✂️ Taglia File",
        tab_convert: "🔄 Converti Formato",
        url_placeholder: "🔗 Incolla qui il link del tuo video o canzone preferita...",
        search_btn: "🔍 Cerca",
        upload_area_title: "Clicca o trascina un file qui",
        upload_area_desc: "Accetta file video e audio",
        file_selected: "📄 File selezionato:",
        file_size: "📦 Dimensione:",
        file_duration: "⏱️ Durata:",
        time_start: "⏱️ Tempo Iniziale:",
        time_end: "⏱️ Tempo Finale:",
        time_format: "Formato: HH:MM:SS",
        estimated_size: "📊 Dimensione stimata del taglio:",
        trim_download_btn: "✂️ Taglia e Scarica",
        convert_to: "🔄 Converti in:",
        select_format: "-- Seleziona un formato --",
        audio_formats: "🎵 Audio",
        video_formats: "🎬 Video",
        convert_btn: "🔄 Converti File",
        processing: "Elaborazione...",
        uploading: "⏳ Caricamento file...",
        converting: "🔄 Conversione formato...",
        trimming: "✂️ Elaborazione video...",
        error_no_file: "❌ Devi prima selezionare un file",
        error_no_format: "❌ Devi selezionare un formato di output",
        error_no_times: "❌ Devi specificare il tempo iniziale e finale",
        error_invalid_time: "❌ Formato tempo non valido. Usa HH:MM:SS (esempio: 00:01:30)",
        error_start_greater: "❌ Il tempo iniziale deve essere minore del tempo finale",
        error_exceeds_duration: "❌ Il tempo finale supera la durata del file",
        success_converted: "✅ Conversione riuscita! Avvio download...",
        success_trimmed: "✅ Taglio riuscito! Avvio download..."
    },
    ru: {
        page_title: "Trimvert - Универсальный медиа-инструмент",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Загружайте, обрезайте и конвертируйте медиа с более чем 1000 платформ в лучшем качестве",
        dark_mode: "Тёмный режим",
        light_mode: "Светлый режим",
        language_label: "Язык",
        tab_url: "🔗 Из URL",
        tab_trim: "✂️ Обрезать файл",
        tab_convert: "🔄 Конвертировать формат",
        url_placeholder: "🔗 Вставьте сюда ссылку на ваше любимое видео или песню...",
        search_btn: "🔍 Поиск",
        upload_area_title: "Нажмите или перетащите файл сюда",
        upload_area_desc: "Принимает видео и аудио файлы",
        file_selected: "📄 Выбранный файл:",
        file_size: "📦 Размер:",
        file_duration: "⏱️ Длительность:",
        time_start: "⏱️ Время начала:",
        time_end: "⏱️ Время окончания:",
        time_format: "Формат: HH:MM:SS",
        estimated_size: "📊 Приблизительный размер обрезки:",
        trim_download_btn: "✂️ Обрезать и скачать",
        convert_to: "🔄 Конвертировать в:",
        select_format: "-- Выберите формат --",
        audio_formats: "🎵 Аудио",
        video_formats: "🎬 Видео",
        convert_btn: "🔄 Конвертировать файл",
        processing: "Обработка...",
        uploading: "⏳ Загрузка файла...",
        converting: "🔄 Конвертация формата...",
        trimming: "✂️ Обработка видео...",
        error_no_file: "❌ Сначала вы должны выбрать файл",
        error_no_format: "❌ Вы должны выбрать формат вывода",
        error_no_times: "❌ Вы должны указать время начала и окончания",
        error_invalid_time: "❌ Неверный формат времени. Используйте HH:MM:SS (пример: 00:01:30)",
        error_start_greater: "❌ Время начала должно быть меньше времени окончания",
        error_exceeds_duration: "❌ Время окончания превышает длительность файла",
        success_converted: "✅ Конвертация успешна! Начинается загрузка...",
        success_trimmed: "✅ Обрезка успешна! Начинается загрузка..."
    },
    zh: {
        page_title: "Trimvert - 通用媒体工具",
        main_title: "✨ Trimvert",
        subtitle: "🎬 从1000多个平台下载、裁剪和转换高质量媒体",
        dark_mode: "暗黑模式",
        light_mode: "明亮模式",
        language_label: "语言",
        tab_url: "🔗 从URL",
        tab_trim: "✂️ 裁剪文件",
        tab_convert: "🔄 转换格式",
        url_placeholder: "🔗 在此粘贴您喜欢的视频或歌曲链接...",
        search_btn: "🔍 搜索",
        upload_area_title: "点击或拖拽文件到这里",
        upload_area_desc: "接受视频和音频文件",
        file_selected: "📄 已选择文件：",
        file_size: "📦 大小：",
        file_duration: "⏱️ 时长：",
        time_start: "⏱️ 开始时间：",
        time_end: "⏱️ 结束时间：",
        time_format: "格式：HH:MM:SS",
        estimated_size: "📊 预估裁剪大小：",
        trim_download_btn: "✂️ 裁剪并下载",
        convert_to: "🔄 转换为：",
        select_format: "-- 选择格式 --",
        audio_formats: "🎵 音频",
        video_formats: "🎬 视频",
        convert_btn: "🔄 转换文件",
        processing: "处理中...",
        uploading: "⏳ 上传文件中...",
        converting: "🔄 转换格式中...",
        trimming: "✂️ 处理视频中...",
        error_no_file: "❌ 您必须先选择一个文件",
        error_no_format: "❌ 您必须选择输出格式",
        error_no_times: "❌ 您必须指定开始和结束时间",
        error_invalid_time: "❌ 时间格式无效。使用 HH:MM:SS（例如：00:01:30）",
        error_start_greater: "❌ 开始时间必须小于结束时间",
        error_exceeds_duration: "❌ 结束时间超过文件时长",
        success_converted: "✅ 转换成功！开始下载...",
        success_trimmed: "✅ 裁剪成功！开始下载..."
    },
    ja: {
        page_title: "Trimvert - ユニバーサルメディアツール",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000以上のプラットフォームから最高品質でメディアをダウンロード、トリミング、変換",
        dark_mode: "ダークモード",
        light_mode: "ライトモード",
        language_label: "言語",
        tab_url: "🔗 URLから",
        tab_trim: "✂️ ファイルをトリミング",
        tab_convert: "🔄 フォーマット変換",
        url_placeholder: "🔗 お気に入りの動画や曲のリンクをここに貼り付けてください...",
        search_btn: "🔍 検索",
        upload_area_title: "ここをクリックするかファイルをドラッグ",
        upload_area_desc: "ビデオとオーディオファイルを受け入れます",
        file_selected: "📄 選択されたファイル：",
        file_size: "📦 サイズ：",
        file_duration: "⏱️ 長さ：",
        time_start: "⏱️ 開始時間：",
        time_end: "⏱️ 終了時間：",
        time_format: "形式：HH:MM:SS",
        estimated_size: "📊 推定トリミングサイズ：",
        trim_download_btn: "✂️ トリミングしてダウンロード",
        convert_to: "🔄 変換先：",
        select_format: "-- フォーマットを選択 --",
        audio_formats: "🎵 オーディオ",
        video_formats: "🎬 ビデオ",
        convert_btn: "🔄 ファイルを変換",
        processing: "処理中...",
        uploading: "⏳ ファイルをアップロード中...",
        converting: "🔄 フォーマットを変換中...",
        trimming: "✂️ ビデオを処理中...",
        error_no_file: "❌ まずファイルを選択する必要があります",
        error_no_format: "❌ 出力フォーマットを選択する必要があります",
        error_no_times: "❌ 開始時間と終了時間を指定する必要があります",
        error_invalid_time: "❌ 無効な時間形式。HH:MM:SSを使用してください（例：00:01:30）",
        error_start_greater: "❌ 開始時間は終了時間より小さくなければなりません",
        error_exceeds_duration: "❌ 終了時間がファイルの長さを超えています",
        success_converted: "✅ 変換成功！ダウンロードを開始...",
        success_trimmed: "✅ トリミング成功！ダウンロードを開始..."
    },
    ko: {
        page_title: "Trimvert - 유니버설 미디어 도구",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000개 이상의 플랫폼에서 최고 품질로 미디어 다운로드, 트리밍 및 변환",
        dark_mode: "다크 모드",
        light_mode: "라이트 모드",
        language_label: "언어",
        tab_url: "🔗 URL에서",
        tab_trim: "✂️ 파일 트리밍",
        tab_convert: "🔄 형식 변환",
        url_placeholder: "🔗 여기에 좋아하는 비디오 또는 노래 링크를 붙여넣으세요...",
        search_btn: "🔍 검색",
        upload_area_title: "여기를 클릭하거나 파일을 드래그하세요",
        upload_area_desc: "비디오 및 오디오 파일 허용",
        file_selected: "📄 선택된 파일:",
        file_size: "📦 크기:",
        file_duration: "⏱️ 길이:",
        time_start: "⏱️ 시작 시간:",
        time_end: "⏱️ 종료 시간:",
        time_format: "형식: HH:MM:SS",
        estimated_size: "📊 예상 트리밍 크기:",
        trim_download_btn: "✂️ 트리밍 및 다운로드",
        convert_to: "🔄 변환 대상:",
        select_format: "-- 형식 선택 --",
        audio_formats: "🎵 오디오",
        video_formats: "🎬 비디오",
        convert_btn: "🔄 파일 변환",
        processing: "처리 중...",
        uploading: "⏳ 파일 업로드 중...",
        converting: "🔄 형식 변환 중...",
        trimming: "✂️ 비디오 처리 중...",
        error_no_file: "❌ 먼저 파일을 선택해야 합니다",
        error_no_format: "❌ 출력 형식을 선택해야 합니다",
        error_no_times: "❌ 시작 및 종료 시간을 지정해야 합니다",
        error_invalid_time: "❌ 잘못된 시간 형식입니다. HH:MM:SS를 사용하세요 (예: 00:01:30)",
        error_start_greater: "❌ 시작 시간은 종료 시간보다 작아야 합니다",
        error_exceeds_duration: "❌ 종료 시간이 파일 길이를 초과합니다",
        success_converted: "✅ 변환 성공! 다운로드 시작...",
        success_trimmed: "✅ 트리밍 성공! 다운로드 시작..."
    },
    ar: {
        page_title: "Trimvert - أداة الوسائط الشاملة",
        main_title: "✨ Trimvert",
        subtitle: "🎬 قم بتنزيل وقص وتحويل الوسائط من أكثر من 1000 منصة بأفضل جودة",
        dark_mode: "الوضع الداكن",
        light_mode: "الوضع الفاتح",
        language_label: "اللغة",
        tab_url: "🔗 من URL",
        tab_trim: "✂️ قص الملف",
        tab_convert: "🔄 تحويل التنسيق",
        url_placeholder: "🔗 الصق هنا رابط الفيديو أو الأغنية المفضلة لديك...",
        search_btn: "🔍 بحث",
        upload_area_title: "انقر أو اسحب ملفًا هنا",
        upload_area_desc: "يقبل ملفات الفيديو والصوت",
        file_selected: "📄 الملف المحدد:",
        file_size: "📦 الحجم:",
        file_duration: "⏱️ المدة:",
        time_start: "⏱️ وقت البداية:",
        time_end: "⏱️ وقت النهاية:",
        time_format: "التنسيق: HH:MM:SS",
        estimated_size: "📊 الحجم التقريبي للقص:",
        trim_download_btn: "✂️ قص وتنزيل",
        convert_to: "🔄 تحويل إلى:",
        select_format: "-- اختر تنسيقًا --",
        audio_formats: "🎵 صوت",
        video_formats: "🎬 فيديو",
        convert_btn: "🔄 تحويل الملف",
        processing: "جاري المعالجة...",
        uploading: "⏳ جاري تحميل الملف...",
        converting: "🔄 جاري تحويل التنسيق...",
        trimming: "✂️ جاري معالجة الفيديو...",
        error_no_file: "❌ يجب عليك أولاً تحديد ملف",
        error_no_format: "❌ يجب عليك تحديد تنسيق الإخراج",
        error_no_times: "❌ يجب عليك تحديد وقت البداية والنهاية",
        error_invalid_time: "❌ تنسيق الوقت غير صالح. استخدم HH:MM:SS (مثال: 00:01:30)",
        error_start_greater: "❌ يجب أن يكون وقت البداية أقل من وقت النهاية",
        error_exceeds_duration: "❌ وقت النهاية يتجاوز مدة الملف",
        success_converted: "✅ التحويل ناجح! بدء التنزيل...",
        success_trimmed: "✅ القص ناجح! بدء التنزيل..."
    },
    // Hindi
    hi: {
        page_title: "Trimvert - यूनिवर्सल मीडिया टूल",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ प्लेटफॉर्म से सर्वोत्तम गुणवत्ता में मीडिया डाउनलोड, ट्रिम और कन्वर्ट करें",
        dark_mode: "डार्क मोड",
        light_mode: "लाइट मोड",
        language_label: "भाषा",
        tab_url: "🔗 URL से",
        tab_trim: "✂️ फ़ाइल ट्रिम करें",
        tab_convert: "🔄 फ़ॉर्मेट बदलें",
        url_placeholder: "🔗 यहाँ अपने पसंदीदा वीडियो या गाने की लिंक पेस्ट करें...",
        search_btn: "🔍 खोजें"
    },
    // Bengali
    bn: {
        page_title: "Trimvert - সর্বজনীন মিডিয়া টুল",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ প্ল্যাটফর্ম থেকে সেরা মানের মিডিয়া ডাউনলোড, ট্রিম এবং রূপান্তর করুন",
        dark_mode: "ডার্ক মোড",
        light_mode: "লাইট মোড",
        language_label: "ভাষা",
        tab_url: "🔗 URL থেকে",
        tab_trim: "✂️ ফাইল ট্রিম করুন",
        tab_convert: "🔄 ফরম্যাট রূপান্তর",
        url_placeholder: "🔗 এখানে আপনার প্রিয় ভিডিও বা গানের লিঙ্ক পেস্ট করুন...",
        search_btn: "🔍 অনুসন্ধান"
    },
    // Turkish
    tr: {
        page_title: "Trimvert - Evrensel Medya Aracı",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ platformdan en iyi kalitede medya indirin, kırpın ve dönüştürün",
        dark_mode: "Karanlık Mod",
        light_mode: "Aydınlık Mod",
        language_label: "Dil",
        tab_url: "🔗 URL'den",
        tab_trim: "✂️ Dosya Kırp",
        tab_convert: "🔄 Format Dönüştür",
        url_placeholder: "🔗 Favori videonuzun veya şarkınızın linkini buraya yapıştırın...",
        search_btn: "🔍 Ara"
    },
    // Vietnamese
    vi: {
        page_title: "Trimvert - Công cụ Đa phương tiện Toàn diện",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Tải xuống, cắt và chuyển đổi phương tiện từ hơn 1000 nền tảng với chất lượng tốt nhất",
        dark_mode: "Chế độ Tối",
        light_mode: "Chế độ Sáng",
        language_label: "Ngôn ngữ",
        tab_url: "🔗 Từ URL",
        tab_trim: "✂️ Cắt Tệp",
        tab_convert: "🔄 Chuyển Đổi Định dạng",
        url_placeholder: "🔗 Dán liên kết video hoặc bài hát yêu thích của bạn vào đây...",
        search_btn: "🔍 Tìm kiếm"
    },
    // Polish
    pl: {
        page_title: "Trimvert - Uniwersalne Narzędzie Multimedialne",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Pobieraj, przycinaj i konwertuj multimedia z ponad 1000 platform w najlepszej jakości",
        dark_mode: "Tryb Ciemny",
        light_mode: "Tryb Jasny",
        language_label: "Język",
        tab_url: "🔗 Z URL",
        tab_trim: "✂️ Przytnij Plik",
        tab_convert: "🔄 Konwertuj Format",
        url_placeholder: "🔗 Wklej tutaj link do ulubionego filmu lub piosenki...",
        search_btn: "🔍 Szukaj"
    },
    // Ukrainian
    uk: {
        page_title: "Trimvert - Універсальний медіа-інструмент",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Завантажуйте, обрізайте та конвертуйте медіа з понад 1000 платформ у найкращій якості",
        dark_mode: "Темний режим",
        light_mode: "Світлий режим",
        language_label: "Мова",
        tab_url: "🔗 З URL",
        tab_trim: "✂️ Обрізати файл",
        tab_convert: "🔄 Конвертувати формат",
        url_placeholder: "🔗 Вставте сюди посилання на ваше улюблене відео або пісню...",
        search_btn: "🔍 Пошук"
    },
    // Dutch
    nl: {
        page_title: "Trimvert - Universeel Media-instrument",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Download, knip en converteer media van meer dan 1000 platforms in de beste kwaliteit",
        dark_mode: "Donkere Modus",
        light_mode: "Lichte Modus",
        language_label: "Taal",
        tab_url: "🔗 Vanaf URL",
        tab_trim: "✂️ Bestand Knippen",
        tab_convert: "🔄 Formaat Converteren",
        url_placeholder: "🔗 Plak hier de link naar je favoriete video of nummer...",
        search_btn: "🔍 Zoeken"
    },
    // Thai
    th: {
        page_title: "Trimvert - เครื่องมือสื่อสากล",
        main_title: "✨ Trimvert",
        subtitle: "🎬 ดาวน์โหลด ตัดต่อ และแปลงสื่อจากแพลตฟอร์มมากกว่า 1000 แห่งในคุณภาพสูงสุด",
        dark_mode: "โหมดมืด",
        light_mode: "โหมดสว่าง",
        language_label: "ภาษา",
        tab_url: "🔗 จาก URL",
        tab_trim: "✂️ ตัดไฟล์",
        tab_convert: "🔄 แปลงรูปแบบ",
        url_placeholder: "🔗 วางลิงก์วิดีโอหรือเพลงโปรดของคุณที่นี่...",
        search_btn: "🔍 ค้นหา"
    },
    // Indonesian
    id: {
        page_title: "Trimvert - Alat Media Universal",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Unduh, potong, dan konversi media dari lebih dari 1000 platform dalam kualitas terbaik",
        dark_mode: "Mode Gelap",
        light_mode: "Mode Terang",
        language_label: "Bahasa",
        tab_url: "🔗 Dari URL",
        tab_trim: "✂️ Potong File",
        tab_convert: "🔄 Konversi Format",
        url_placeholder: "🔗 Tempel tautan video atau lagu favorit Anda di sini...",
        search_btn: "🔍 Cari"
    },
    // Swedish
    sv: {
        page_title: "Trimvert - Universellt Mediaverktyg",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Ladda ner, klipp och konvertera media från över 1000 plattformar i bästa kvalitet",
        dark_mode: "Mörkt Läge",
        light_mode: "Ljust Läge",
        language_label: "Språk",
        tab_url: "🔗 Från URL",
        tab_trim: "✂️ Klipp Fil",
        tab_convert: "🔄 Konvertera Format",
        url_placeholder: "🔗 Klistra in länken till din favoritvideo eller låt här...",
        search_btn: "🔍 Sök"
    },
    // Romanian
    ro: {
        page_title: "Trimvert - Instrument Media Universal",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Descărcați, tăiați și convertiți media de pe peste 1000 de platforme în cea mai bună calitate",
        dark_mode: "Mod Întunecat",
        light_mode: "Mod Luminos",
        language_label: "Limbă",
        tab_url: "🔗 Din URL",
        tab_trim: "✂️ Tăiere Fișier",
        tab_convert: "🔄 Conversie Format",
        url_placeholder: "🔗 Lipiți aici linkul către videoclipul sau melodia dvs. preferată...",
        search_btn: "🔍 Căutare"
    },
    // Czech
    cs: {
        page_title: "Trimvert - Univerzální Mediální Nástroj",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Stahujte, střihejte a konvertujte média z více než 1000 platforem v nejlepší kvalitě",
        dark_mode: "Tmavý Režim",
        light_mode: "Světlý Režim",
        language_label: "Jazyk",
        tab_url: "🔗 Z URL",
        tab_trim: "✂️ Střih Souboru",
        tab_convert: "🔄 Převod Formátu",
        url_placeholder: "🔗 Vložte sem odkaz na své oblíbené video nebo píseň...",
        search_btn: "🔍 Hledat"
    },
    // Greek
    el: {
        page_title: "Trimvert - Καθολικό Εργαλείο Πολυμέσων",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Λήψη, περικοπή και μετατροπή πολυμέσων από πάνω από 1000 πλατφόρμες στην καλύτερη ποιότητα",
        dark_mode: "Σκοτεινή Λειτουργία",
        light_mode: "Φωτεινή Λειτουργία",
        language_label: "Γλώσσα",
        tab_url: "🔗 Από URL",
        tab_trim: "✂️ Περικοπή Αρχείου",
        tab_convert: "🔄 Μετατροπή Μορφής",
        url_placeholder: "🔗 Επικολλήστε εδώ τον σύνδεσμο του αγαπημένου σας βίντεο ή τραγουδιού...",
        search_btn: "🔍 Αναζήτηση"
    },
    // Hungarian
    hu: {
        page_title: "Trimvert - Univerzális Médiakesztyű",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Töltsön le, vágjon és konvertáljon médiát több mint 1000 platformról a legjobb minőségben",
        dark_mode: "Sötét Mód",
        light_mode: "Világos Mód",
        language_label: "Nyelv",
        tab_url: "🔗 URL-ről",
        tab_trim: "✂️ Fájl Vágás",
        tab_convert: "🔄 Formátum Konvertálás",
        url_placeholder: "🔗 Illessze be ide kedvenc videójának vagy dalának linkjét...",
        search_btn: "🔍 Keresés"
    },
    // Finnish
    fi: {
        page_title: "Trimvert - Yleinen Mediatyökalu",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Lataa, leikkaa ja muunna mediaa yli 1000 alustalta parhaalla laadulla",
        dark_mode: "Tumma Tila",
        light_mode: "Vaalea Tila",
        language_label: "Kieli",
        tab_url: "🔗 URL:stä",
        tab_trim: "✂️ Leikkaa Tiedosto",
        tab_convert: "🔄 Muunna Muoto",
        url_placeholder: "🔗 Liitä tähän suosikki videosi tai kappaleesi linkki...",
        search_btn: "🔍 Hae"
    },
    // Norwegian
    no: {
        page_title: "Trimvert - Universelt Medieverktøy",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Last ned, klipp og konverter media fra over 1000 plattformer i beste kvalitet",
        dark_mode: "Mørk Modus",
        light_mode: "Lys Modus",
        language_label: "Språk",
        tab_url: "🔗 Fra URL",
        tab_trim: "✂️ Klipp Fil",
        tab_convert: "🔄 Konverter Format",
        url_placeholder: "🔗 Lim inn lenken til favorittvidéoen eller sangen din her...",
        search_btn: "🔍 Søk"
    },
    // Danish
    da: {
        page_title: "Trimvert - Universelt Medieværktøj",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Download, klip og konverter medier fra over 1000 platforme i bedste kvalitet",
        dark_mode: "Mørk Tilstand",
        light_mode: "Lys Tilstand",
        language_label: "Sprog",
        tab_url: "🔗 Fra URL",
        tab_trim: "✂️ Klip Fil",
        tab_convert: "🔄 Konverter Format",
        url_placeholder: "🔗 Indsæt linket til din foretrukne video eller sang her...",
        search_btn: "🔍 Søg"
    },
    // Hebrew
    he: {
        page_title: "Trimvert - כלי מדיה אוניברסלי",
        main_title: "✨ Trimvert",
        subtitle: "🎬 הורד, גזור והמר מדיה מיותר מ-1000 פלטפורמות באיכות הטובה ביותר",
        dark_mode: "מצב כהה",
        light_mode: "מצב בהיר",
        language_label: "שפה",
        tab_url: "🔗 מ-URL",
        tab_trim: "✂️ גזור קובץ",
        tab_convert: "🔄 המר פורמט",
        url_placeholder: "🔗 הדבק כאן את הקישור לסרטון או לשיר האהוב עליך...",
        search_btn: "🔍 חפש"
    },
    // Persian
    fa: {
        page_title: "Trimvert - ابزار رسانه جهانی",
        main_title: "✨ Trimvert",
        subtitle: "🎬 دانلود، برش و تبدیل رسانه از بیش از 1000 پلتفرم با بهترین کیفیت",
        dark_mode: "حالت تاریک",
        light_mode: "حالت روشن",
        language_label: "زبان",
        tab_url: "🔗 از URL",
        tab_trim: "✂️ برش فایل",
        tab_convert: "🔄 تبدیل فرمت",
        url_placeholder: "🔗 لینک ویدیو یا آهنگ مورد علاقه خود را اینجا وارد کنید...",
        search_btn: "🔍 جستجو"
    },
    // Malay
    ms: {
        page_title: "Trimvert - Alat Media Sejagat",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Muat turun, potong dan tukar media dari lebih 1000 platform dalam kualiti terbaik",
        dark_mode: "Mod Gelap",
        light_mode: "Mod Terang",
        language_label: "Bahasa",
        tab_url: "🔗 Dari URL",
        tab_trim: "✂️ Potong Fail",
        tab_convert: "🔄 Tukar Format",
        url_placeholder: "🔗 Tampal pautan video atau lagu kegemaran anda di sini...",
        search_btn: "🔍 Cari"
    },
    // Swahili
    sw: {
        page_title: "Trimvert - Zana ya Vyombo vya Habari ya Ulimwengu",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Pakua, kata na badilisha vyombo vya habari kutoka majukwaa zaidi ya 1000 kwa ubora bora",
        dark_mode: "Hali ya Giza",
        light_mode: "Hali ya Mwanga",
        language_label: "Lugha",
        tab_url: "🔗 Kutoka URL",
        tab_trim: "✂️ Kata Faili",
        tab_convert: "🔄 Badilisha Muundo",
        url_placeholder: "🔗 Bandika kiungo cha video au wimbo wako unaopenda hapa...",
        search_btn: "🔍 Tafuta"
    },
    // Tamil
    ta: {
        page_title: "Trimvert - உலகளாவிய ஊடக கருவி",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ தளங்களில் இருந்து சிறந்த தரத்தில் ஊடகத்தை பதிவிறக்கம் செய்யுங்கள், வெட்டுங்கள் மற்றும் மாற்றுங்கள்",
        dark_mode: "இருள் பயன்முறை",
        light_mode: "ஒளி பயன்முறை",
        language_label: "மொழி",
        tab_url: "🔗 URL இலிருந்து",
        tab_trim: "✂️ கோப்பை வெட்டவும்",
        tab_convert: "🔄 வடிவத்தை மாற்றவும்",
        url_placeholder: "🔗 உங்கள் விருப்பமான வீடியோ அல்லது பாடலின் இணைப்பை இங்கே ஒட்டவும்...",
        search_btn: "🔍 தேடு"
    },
    // Telugu
    te: {
        page_title: "Trimvert - సార్వత్రిక మీడియా సాధనం",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ ప్లాట్‌ఫారమ్‌ల నుండి అత్యుత్తమ నాణ్యతతో మీడియాను డౌన్‌లోడ్ చేయండి, కత్తిరించండి మరియు మార్చండి",
        dark_mode: "చీకటి మోడ్",
        light_mode: "లైట్ మోడ్",
        language_label: "భాష",
        tab_url: "🔗 URL నుండి",
        tab_trim: "✂️ ఫైల్ కత్తిరించండి",
        tab_convert: "🔄 ఫార్మాట్ మార్చండి",
        url_placeholder: "🔗 మీకు ఇష్టమైన వీడియో లేదా పాట లింక్‌ను ఇక్కడ అతికించండి...",
        search_btn: "🔍 శోధించండి"
    },
    // Marathi
    mr: {
        page_title: "Trimvert - सार्वत्रिक मीडिया साधन",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ प्लॅटफॉर्मवरून उत्तम गुणवत्तेत मीडिया डाउनलोड करा, ट्रिम करा आणि रूपांतरित करा",
        dark_mode: "गडद मोड",
        light_mode: "प्रकाश मोड",
        language_label: "भाषा",
        tab_url: "🔗 URL वरून",
        tab_trim: "✂️ फाइल ट्रिम करा",
        tab_convert: "🔄 फॉरमॅट रूपांतरित करा",
        url_placeholder: "🔗 तुमच्या आवडत्या व्हिडिओ किंवा गाण्याची लिंक येथे पेस्ट करा...",
        search_btn: "🔍 शोधा"
    },
    // Urdu
    ur: {
        page_title: "Trimvert - عالمگیر میڈیا ٹول",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ پلیٹ فارمز سے بہترین معیار میں میڈیا ڈاؤن لوڈ، ٹرم اور تبدیل کریں",
        dark_mode: "ڈارک موڈ",
        light_mode: "لائٹ موڈ",
        language_label: "زبان",
        tab_url: "🔗 URL سے",
        tab_trim: "✂️ فائل ٹرم کریں",
        tab_convert: "🔄 فارمیٹ تبدیل کریں",
        url_placeholder: "🔗 اپنی پسندیدہ ویڈیو یا گانے کا لنک یہاں پیسٹ کریں...",
        search_btn: "🔍 تلاش کریں"
    },
    // Catalan
    ca: {
        page_title: "Trimvert - Eina Multimèdia Universal",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Descarrega, retalla i converteix mitjans de més de 1000 plataformes amb la millor qualitat",
        dark_mode: "Mode Fosc",
        light_mode: "Mode Clar",
        language_label: "Idioma",
        tab_url: "🔗 Des d'URL",
        tab_trim: "✂️ Retallar Fitxer",
        tab_convert: "🔄 Convertir Format",
        url_placeholder: "🔗 Enganxa aquí l'enllaç del teu vídeo o cançó preferida...",
        search_btn: "🔍 Cerca"
    },
    // Slovak
    sk: {
        page_title: "Trimvert - Univerzálny Mediálny Nástroj",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Sťahujte, strihajte a konvertujte médiá z viac ako 1000 platforiem v najlepšej kvalite",
        dark_mode: "Tmavý Režim",
        light_mode: "Svetlý Režim",
        language_label: "Jazyk",
        tab_url: "🔗 Z URL",
        tab_trim: "✂️ Strih Súboru",
        tab_convert: "🔄 Prevod Formátu",
        url_placeholder: "🔗 Vložte sem odkaz na svoje obľúbené video alebo pieseň...",
        search_btn: "🔍 Hľadať"
    },
    // Bulgarian
    bg: {
        page_title: "Trimvert - Универсален Медиен Инструмент",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Изтегляйте, отрязвайте и конвертирайте медия от повече от 1000 платформи в най-високо качество",
        dark_mode: "Тъмен Режим",
        light_mode: "Светъл Режим",
        language_label: "Език",
        tab_url: "🔗 От URL",
        tab_trim: "✂️ Отрязване на Файл",
        tab_convert: "🔄 Конвертиране на Формат",
        url_placeholder: "🔗 Поставете тук връзката към любимото си видео или песен...",
        search_btn: "🔍 Търсене"
    },
    // Serbian
    sr: {
        page_title: "Trimvert - Универзални Медијски Алат",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Преузмите, исеците и конвертујте медије са преко 1000 платформи у најбољем квалитету",
        dark_mode: "Тамни Режим",
        light_mode: "Светли Режим",
        language_label: "Језик",
        tab_url: "🔗 Од URL",
        tab_trim: "✂️ Исецање Фајла",
        tab_convert: "🔄 Конверзија Формата",
        url_placeholder: "🔗 Налепите овде везу до свог омиљеног видео записа или песме...",
        search_btn: "🔍 Претрага"
    },
    // Croatian
    hr: {
        page_title: "Trimvert - Univerzalni Medijski Alat",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Preuzmite, izrežite i konvertirajte medije s više od 1000 platformi u najboljoj kvaliteti",
        dark_mode: "Tamni Način",
        light_mode: "Svijetli Način",
        language_label: "Jezik",
        tab_url: "🔗 Od URL-a",
        tab_trim: "✂️ Rezanje Datoteke",
        tab_convert: "🔄 Konverzija Formata",
        url_placeholder: "🔗 Zalijepite ovdje poveznicu na svoj omiljeni video ili pjesmu...",
        search_btn: "🔍 Pretraži"
    },
    lt: {
        page_title: "Trimvert - Universali Medijos Priemonė",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Atsisiųskite, apkarpykite ir konvertuokite mediją iš daugiau nei 1000 platformų",
        dark_mode: "Tamsusis Režimas",
        light_mode: "Šviesiasis Režimas",
        language_label: "Kalba",
        tab_url: "🔗 Iš URL",
        tab_trim: "✂️ Kirpti Failą",
        tab_convert: "🔄 Konvertuoti Formatą",
        url_placeholder: "🔗 Įklijuokite savo mėgstamo vaizdo ar dainos nuorodą čia...",
        search_btn: "🔍 Ieškoti"
    },
    lv: {
        page_title: "Trimvert - Universāls Mediju Rīks",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Lejupielādējiet, apgrieziet un konvertējiet medijus no vairāk nekā 1000 platformām",
        dark_mode: "Tumšais Režīms",
        light_mode: "Gaišais Režīms",
        language_label: "Valoda",
        tab_url: "🔗 No URL",
        tab_trim: "✂️ Apgriezt Failu",
        tab_convert: "🔄 Konvertēt Formātu",
        url_placeholder: "🔗 Ielīmējiet savas iecienītākās video vai dziesmas saiti šeit...",
        search_btn: "🔍 Meklēt"
    },
    et: {
        page_title: "Trimvert - Universaalne Meediatööriist",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Laadige alla, lõigake ja teisendage meediat üle 1000 platvormilt",
        dark_mode: "Tume Režiim",
        light_mode: "Hele Režiim",
        language_label: "Keel",
        tab_url: "🔗 URL-ist",
        tab_trim: "✂️ Lõika Faili",
        tab_convert: "🔄 Teisenda Formaati",
        url_placeholder: "🔗 Kleebi siia oma lemmik video või laulu link...",
        search_btn: "🔍 Otsi"
    },
    sl: {
        page_title: "Trimvert - Univerzalno Medijsko Orodje",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Prenesite, obrežite in pretvorite medije z več kot 1000 platform",
        dark_mode: "Temni Način",
        light_mode: "Svetli Način",
        language_label: "Jezik",
        tab_url: "🔗 Iz URL",
        tab_trim: "✂️ Obreži Datoteko",
        tab_convert: "🔄 Pretvori Format",
        url_placeholder: "🔗 Prilepite povezavo do svojega najljubšega videoposnetka ali pesmi tukaj...",
        search_btn: "🔍 Iskanje"
    },
    sq: {
        page_title: "Trimvert - Mjet Universal Mediash",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Shkarkoni, pritni dhe konvertoni media nga mbi 1000 platforma",
        dark_mode: "Modaliteti i Errët",
        light_mode: "Modaliteti i Ndritshëm",
        language_label: "Gjuha",
        tab_url: "🔗 Nga URL",
        tab_trim: "✂️ Prit Skedarin",
        tab_convert: "🔄 Konverto Formatin",
        url_placeholder: "🔗 Ngjit këtu lidhjen e videos ose këngës tënde të preferuar...",
        search_btn: "🔍 Kërko"
    },
    mk: {
        page_title: "Trimvert - Универзална Медиумска Алатка",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Преземете, исечете и конвертирајте медиуми од повеќе од 1000 платформи",
        dark_mode: "Темен Режим",
        light_mode: "Светол Режим",
        language_label: "Јазик",
        tab_url: "🔗 Од URL",
        tab_trim: "✂️ Исечи Датотека",
        tab_convert: "🔄 Конвертирај Формат",
        url_placeholder: "🔗 Залепете ја врската до вашето омилено видео или песна овде...",
        search_btn: "🔍 Барај"
    },
    bs: {
        page_title: "Trimvert - Univerzalni Medijski Alat",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Preuzmite, izrežite i konvertujte medije sa više od 1000 platformi",
        dark_mode: "Tamni Način",
        light_mode: "Svijetli Način",
        language_label: "Jezik",
        tab_url: "🔗 Sa URL-a",
        tab_trim: "✂️ Rezanje Fajla",
        tab_convert: "🔄 Konverzija Formata",
        url_placeholder: "🔗 Zalijepite ovdje link na svoj omiljeni video ili pjesmu...",
        search_btn: "🔍 Pretraži"
    },
    is: {
        page_title: "Trimvert - Alhliða Miðlatól",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Sæktu, klipptu og umbreyttu miðlum frá yfir 1000 vettvangi",
        dark_mode: "Dökkt Stillingu",
        light_mode: "Ljóst Stillingu",
        language_label: "Tungumál",
        tab_url: "🔗 Frá URL",
        tab_trim: "✂️ Klippa Skrá",
        tab_convert: "🔄 Umbreyta Sniði",
        url_placeholder: "🔗 Límdu hlekkinn á uppáhalds myndband eða lag þitt hér...",
        search_btn: "🔍 Leita"
    },
    ga: {
        page_title: "Trimvert - Uirlis Uilíoch Meán",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Íoslódáil, bearr agus tiontaigh meáin ó níos mó ná 1000 ardán",
        dark_mode: "Mód Dorcha",
        light_mode: "Mód Geal",
        language_label: "Teanga",
        tab_url: "🔗 Ó URL",
        tab_trim: "✂️ Bearr Comhad",
        tab_convert: "🔄 Tiontaigh Formáid",
        url_placeholder: "🔗 Greamaigh nasc do físeán nó amhrán is fearr leat anseo...",
        search_btn: "🔍 Cuardaigh"
    },
    cy: {
        page_title: "Trimvert - Offeryn Cyfryngau Cyffredinol",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Lawrlwythwch, tociwch a thrawsnewidiwch gyfryngau o dros 1000 o lwyfannau",
        dark_mode: "Modd Tywyll",
        light_mode: "Modd Golau",
        language_label: "Iaith",
        tab_url: "🔗 O URL",
        tab_trim: "✂️ Tocio Ffeil",
        tab_convert: "🔄 Trosi Fformat",
        url_placeholder: "🔗 Gludwch ddolen eich hoff fideo neu gân yma...",
        search_btn: "🔍 Chwilio"
    },
    eu: {
        page_title: "Trimvert - Multimedia Tresna Unibertsala",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Deskargatu, moztu eta bihurtu multimedia 1000 plataforma baino gehiagotatik",
        dark_mode: "Modu Iluna",
        light_mode: "Modu Argia",
        language_label: "Hizkuntza",
        tab_url: "🔗 URL-tik",
        tab_trim: "✂️ Fitxategia Moztu",
        tab_convert: "🔄 Formatua Bihurtu",
        url_placeholder: "🔗 Itsatsi hemen zure bideo edo abesti gogokoenaren esteka...",
        search_btn: "🔍 Bilatu"
    },
    gl: {
        page_title: "Trimvert - Ferramenta Multimedia Universal",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Descarga, recorta e converte multimedia de máis de 1000 plataformas",
        dark_mode: "Modo Escuro",
        light_mode: "Modo Claro",
        language_label: "Idioma",
        tab_url: "🔗 Desde URL",
        tab_trim: "✂️ Recortar Ficheiro",
        tab_convert: "🔄 Converter Formato",
        url_placeholder: "🔗 Pega aquí a ligazón do teu vídeo ou canción favorita...",
        search_btn: "🔍 Buscar"
    },
    af: {
        page_title: "Trimvert - Universele Media Instrument",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Laai af, sny en omskep media van meer as 1000 platforms",
        dark_mode: "Donker Modus",
        light_mode: "Ligte Modus",
        language_label: "Taal",
        tab_url: "🔗 Van URL",
        tab_trim: "✂️ Sny Lêer",
        tab_convert: "🔄 Omskep Formaat",
        url_placeholder: "🔗 Plak jou gunsteling video of liedjie skakel hier...",
        search_btn: "🔍 Soek"
    },
    zu: {
        page_title: "Trimvert - Ithuluzi Lemidiya Yonke",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Landa, sika futhi uguqule imidiya kusuka ezinkundleni ezingaphezu kuka-1000",
        dark_mode: "Imodi Emnyama",
        light_mode: "Imodi Ekhanyayo",
        language_label: "Ulimi",
        tab_url: "🔗 Kusuka ku-URL",
        tab_trim: "✂️ Sika Ifayela",
        tab_convert: "🔄 Guqula Ifomethi",
        url_placeholder: "🔗 Namathisela isixhumanisi sevidiyo noma ingoma oyithandayo lapha...",
        search_btn: "🔍 Sesha"
    },
    xh: {
        page_title: "Trimvert - Isixhobo Semidiya Jikelele",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Khuphela, sika uze uguqule imidiya ukusuka kumaqonga angaphezu kwe-1000",
        dark_mode: "Imowudi Emnyama",
        light_mode: "Imowudi Ekhanyayo",
        language_label: "Ulwimi",
        tab_url: "🔗 Ukusuka kwi-URL",
        tab_trim: "✂️ Sika Ifayile",
        tab_convert: "🔄 Guqula Ifomathi",
        url_placeholder: "🔗 Ncamathisela ikhonkco levidiyo okanye ingoma oyithandayo apha...",
        search_btn: "🔍 Khangela"
    },
    am: {
        page_title: "Trimvert - አጠቃላይ ሚዲያ መሳሪያ",
        main_title: "✨ Trimvert",
        subtitle: "🎬 ከ1000 በላይ መድረኮች ሚዲያ አውርድ፣ ቁረጥ እና ለውጥ",
        dark_mode: "ጨለማ ሁኔታ",
        light_mode: "ብርሃን ሁኔታ",
        language_label: "ቋንቋ",
        tab_url: "🔗 ከURL",
        tab_trim: "✂️ ፋይል ቁረጥ",
        tab_convert: "🔄 ቅርጸት ለውጥ",
        url_placeholder: "🔗 የምትወደውን ቪዲዮ ወይም ዘፈን አገናኝ እዚህ ለጥፍ...",
        search_btn: "🔍 ፈልግ"
    },
    ha: {
        page_title: "Trimvert - Kayan Aikin Kafofin Watsa Labarai",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Sauke, yanke kuma canza kafofin watsa labarai daga dandamali sama da 1000",
        dark_mode: "Yanayin Duhu",
        light_mode: "Yanayin Haske",
        language_label: "Harshe",
        tab_url: "🔗 Daga URL",
        tab_trim: "✂️ Yanke Fayil",
        tab_convert: "🔄 Canza Tsari",
        url_placeholder: "🔗 Manna hanyar haɗin bidiyo ko waƙar da kake so a nan...",
        search_btn: "🔍 Bincika"
    },
    yo: {
        page_title: "Trimvert - Ohun Elo Media Gbogbogbo",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Gba sile, ge ati yi media pada lati awọn syeed to ju 1000 lọ",
        dark_mode: "Ipo Dudu",
        light_mode: "Ipo Imọlẹ",
        language_label: "Ede",
        tab_url: "🔗 Lati URL",
        tab_trim: "✂️ Ge Faili",
        tab_convert: "🔄 Yi Ọna Kika Pada",
        url_placeholder: "🔗 Lẹ ọpọlọpọ fidio tabi orin ayanfẹ rẹ nibi...",
        search_btn: "🔍 Wa"
    },
    ig: {
        page_title: "Trimvert - Ngwa Media Zuru Oke",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Budata, bee ma gbanwee media site na ikpo okwu karịrị 1000",
        dark_mode: "Ọnọdụ Ọchịchịrị",
        light_mode: "Ọnọdụ Ìhè",
        language_label: "Asụsụ",
        tab_url: "🔗 Site na URL",
        tab_trim: "✂️ Bee Faịlụ",
        tab_convert: "🔄 Gbanwee Usoro",
        url_placeholder: "🔗 Tinye njikọ vidiyo ma ọ bụ egwu kacha amasị gị ebe a...",
        search_btn: "🔍 Chọọ"
    },
    km: {
        page_title: "Trimvert - ឧបករណ៍ប្រព័ន្ធផ្សព្វផ្សាយសកល",
        main_title: "✨ Trimvert",
        subtitle: "🎬 ទាញយក កាត់ និងបំលែងប្រព័ន្ធផ្សព្វផ្សាយពីវេទិកាលើសពី 1000",
        dark_mode: "របៀបងងឹត",
        light_mode: "របៀបភ្លឺ",
        language_label: "ភាសា",
        tab_url: "🔗 ពី URL",
        tab_trim: "✂️ កាត់ឯកសារ",
        tab_convert: "🔄 បំលែងទ្រង់ទ្រាយ",
        url_placeholder: "🔗 បិទភ្ជាប់តំណវីដេអូ ឬបទចម្រៀងដែលអ្នកចូលចិត្តនៅទីនេះ...",
        search_btn: "🔍 ស្វែងរក"
    },
    lo: {
        page_title: "Trimvert - ເຄື່ອງມືສື່ສາກົນ",
        main_title: "✨ Trimvert",
        subtitle: "🎬 ດາວໂຫຼດ, ຕັດ ແລະ ແປງສື່ຈາກແພລດຟອມຫຼາຍກວ່າ 1000",
        dark_mode: "ໂໝດມືດ",
        light_mode: "ໂໝດສະຫວ່າງ",
        language_label: "ພາສາ",
        tab_url: "🔗 ຈາກ URL",
        tab_trim: "✂️ ຕັດໄຟລ໌",
        tab_convert: "🔄 ແປງຮູບແບບ",
        url_placeholder: "🔗 ວາງລິ້ງວິດີໂອ ຫຼື ເພງທີ່ທ່ານມັກຢູ່ທີ່ນີ້...",
        search_btn: "🔍 ຊອກຫາ"
    },
    my: {
        page_title: "Trimvert - Universal Media ကိရိယာ",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000 ကျော် platform များမှ media ဒေါင်းလုပ်၊ ဖြတ်တောက်၊ ပြောင်းလဲပါ",
        dark_mode: "အမှောင် မုဒ်",
        light_mode: "အလင်း မုဒ်",
        language_label: "ဘာသာစကား",
        tab_url: "🔗 URL မှ",
        tab_trim: "✂️ ဖိုင်ဖြတ်မည်",
        tab_convert: "🔄 ပုံစံပြောင်းမည်",
        url_placeholder: "🔗 သင်အကြိုက်ဆုံး ဗီဒီယို သို့မဟုတ် သီချင်းလင့်ကို ဤနေရာတွင် ကူးထည့်ပါ...",
        search_btn: "🔍 ရှာဖွေမည်"
    },
    ne: {
        page_title: "Trimvert - सार्वभौमिक मिडिया उपकरण",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000 भन्दा बढी प्लेटफर्महरूबाट मिडिया डाउनलोड, ट्रिम र रूपान्तरण गर्नुहोस्",
        dark_mode: "अँध्यारो मोड",
        light_mode: "उज्यालो मोड",
        language_label: "भाषा",
        tab_url: "🔗 URL बाट",
        tab_trim: "✂️ फाइल काट्नुहोस्",
        tab_convert: "🔄 ढाँचा रूपान्तरण",
        url_placeholder: "🔗 आफ्नो मनपर्ने भिडियो वा गीतको लिङ्क यहाँ टाँस्नुहोस्...",
        search_btn: "🔍 खोज्नुहोस्"
    },
    si: {
        page_title: "Trimvert - විශ්වීය මාධ්‍ය මෙවලම",
        main_title: "✨ Trimvert",
        subtitle: "🎬 වේදිකා 1000කට වඩා වැඩි ගණනකින් මාධ්‍ය බාගත කරන්න, කපන්න සහ පරිවර්තනය කරන්න",
        dark_mode: "අඳුරු ප්‍රකාරය",
        light_mode: "දීප්ත ප්‍රකාරය",
        language_label: "භාෂාව",
        tab_url: "🔗 URL වලින්",
        tab_trim: "✂️ ගොනුව කපන්න",
        tab_convert: "🔄 ආකෘතිය පරිවර්තනය",
        url_placeholder: "🔗 ඔබේ ප්‍රියතම වීඩියෝ හෝ ගීතයේ සබැඳිය මෙහි අලවන්න...",
        search_btn: "🔍 සොයන්න"
    },
    kn: {
        page_title: "Trimvert - ಸಾರ್ವತ್ರಿಕ ಮಾಧ್ಯಮ ಸಾಧನ",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್‌ಗಳಿಂದ ಮಾಧ್ಯಮವನ್ನು ಡೌನ್‌ಲೋಡ್, ಟ್ರಿಮ್ ಮತ್ತು ಪರಿವರ್ತಿಸಿ",
        dark_mode: "ಡಾರ್ಕ್ ಮೋಡ್",
        light_mode: "ಲೈಟ್ ಮೋಡ್",
        language_label: "ಭಾಷೆ",
        tab_url: "🔗 URL ನಿಂದ",
        tab_trim: "✂️ ಫೈಲ್ ಟ್ರಿಮ್ ಮಾಡಿ",
        tab_convert: "🔄 ಫಾರ್ಮ್ಯಾಟ್ ಪರಿವರ್ತಿಸಿ",
        url_placeholder: "🔗 ನಿಮ್ಮ ಮೆಚ್ಚಿನ ವೀಡಿಯೊ ಅಥವಾ ಹಾಡಿನ ಲಿಂಕ್ ಅನ್ನು ಇಲ್ಲಿ ಅಂಟಿಸಿ...",
        search_btn: "🔍 ಹುಡುಕಿ"
    },
    ml: {
        page_title: "Trimvert - സാർവത്രിക മീഡിയ ഉപകരണം",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000-ലധികം പ്ലാറ്റ്‌ഫോമുകളിൽ നിന്ന് മീഡിയ ഡൗൺലോഡ് ചെയ്യുക, ട്രിം ചെയ്യുക, പരിവർത്തനം ചെയ്യുക",
        dark_mode: "ഡാർക്ക് മോഡ്",
        light_mode: "ലൈറ്റ് മോഡ്",
        language_label: "ഭാഷ",
        tab_url: "🔗 URL-ൽ നിന്ന്",
        tab_trim: "✂️ ഫയൽ ട്രിം ചെയ്യുക",
        tab_convert: "🔄 ഫോർമാറ്റ് പരിവർത്തനം",
        url_placeholder: "🔗 നിങ്ങളുടെ പ്രിയപ്പെട്ട വീഡിയോ അല്ലെങ്കിൽ ഗാനത്തിന്റെ ലിങ്ക് ഇവിടെ ഒട്ടിക്കുക...",
        search_btn: "🔍 തിരയുക"
    },
    gu: {
        page_title: "Trimvert - સાર્વત્રિક મીડિયા સાધન",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ પ્લેટફોર્મ્સથી મીડિયા ડાઉનલોડ, ટ્રિમ અને કન્વર્ટ કરો",
        dark_mode: "ડાર્ક મોડ",
        light_mode: "લાઇટ મોડ",
        language_label: "ભાષા",
        tab_url: "🔗 URL થી",
        tab_trim: "✂️ ફાઇલ ટ્રિમ કરો",
        tab_convert: "🔄 ફોર્મેટ કન્વર્ટ કરો",
        url_placeholder: "🔗 તમારા મનપસંદ વિડિઓ અથવા ગીતની લિંક અહીં પેસ્ટ કરો...",
        search_btn: "🔍 શોધો"
    },
    pa: {
        page_title: "Trimvert - ਯੂਨੀਵਰਸਲ ਮੀਡੀਆ ਟੂਲ",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ ਪਲੇਟਫਾਰਮਾਂ ਤੋਂ ਮੀਡੀਆ ਡਾਊਨਲੋਡ, ਟ੍ਰਿਮ ਅਤੇ ਕਨਵਰਟ ਕਰੋ",
        dark_mode: "ਡਾਰਕ ਮੋਡ",
        light_mode: "ਲਾਈਟ ਮੋਡ",
        language_label: "ਭਾਸ਼ਾ",
        tab_url: "🔗 URL ਤੋਂ",
        tab_trim: "✂️ ਫਾਈਲ ਟ੍ਰਿਮ ਕਰੋ",
        tab_convert: "🔄 ਫਾਰਮੈਟ ਕਨਵਰਟ ਕਰੋ",
        url_placeholder: "🔗 ਆਪਣੀ ਮਨਪਸੰਦ ਵੀਡੀਓ ਜਾਂ ਗੀਤ ਦਾ ਲਿੰਕ ਇੱਥੇ ਪੇਸਟ ਕਰੋ...",
        search_btn: "🔍 ਖੋਜੋ"
    },
    sd: {
        page_title: "Trimvert - آفاقي ميڊيا اوزار",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ پليٽ فارمن مان ميڊيا ڊائون لوڊ، ٽرم ۽ تبديل کريو",
        dark_mode: "ڊارڪ موڊ",
        light_mode: "لائيٽ موڊ",
        language_label: "ٻولي",
        tab_url: "🔗 URL کان",
        tab_trim: "✂️ فائل ٽرم کريو",
        tab_convert: "🔄 فارميٽ تبديل کريو",
        url_placeholder: "🔗 پنهنجي پسنديده وڊيو يا گيت جو لنڪ هتي پيسٽ کريو...",
        search_btn: "🔍 ڳوليو"
    },
    ps: {
        page_title: "Trimvert - نړیوال رسنیزه وسیله",
        main_title: "✨ Trimvert",
        subtitle: "🎬 له 1000+ پلیټ فارمونو څخه رسنۍ ډاونلوډ، ټریم او تبدیل کړئ",
        dark_mode: "تیاره موډ",
        light_mode: "روښانه موډ",
        language_label: "ژبه",
        tab_url: "🔗 له URL څخه",
        tab_trim: "✂️ فایل ټریم کړئ",
        tab_convert: "🔄 بڼه بدله کړئ",
        url_placeholder: "🔗 خپل خوښ ویډیو یا سندرې لینک دلته پیسټ کړئ...",
        search_btn: "🔍 لټون"
    },
    ku: {
        page_title: "Trimvert - ئامرازی میدیای گشتی",
        main_title: "✨ Trimvert",
        subtitle: "🎬 میدیا لە زیاتر لە 1000 پلاتفۆرم دابەزێنە، ببڕە و بگۆڕە",
        dark_mode: "دۆخی تاریک",
        light_mode: "دۆخی ڕووناک",
        language_label: "زمان",
        tab_url: "🔗 لە URL",
        tab_trim: "✂️ فایل ببڕە",
        tab_convert: "🔄 فۆرمات بگۆڕە",
        url_placeholder: "🔗 لینکی ڤیدیۆ یان گۆرانی دڵخوازت لێرە بلکێنە...",
        search_btn: "🔍 بگەڕێ"
    },
    az: {
        page_title: "Trimvert - Universal Media Aləti",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000-dən çox platformadan media yükləyin, kəsin və çevirin",
        dark_mode: "Qaranlıq Rejim",
        light_mode: "İşıqlı Rejim",
        language_label: "Dil",
        tab_url: "🔗 URL-dən",
        tab_trim: "✂️ Faylı Kəs",
        tab_convert: "🔄 Formatı Çevir",
        url_placeholder: "🔗 Sevimli video və ya mahnınızın linkini buraya yapışdırın...",
        search_btn: "🔍 Axtar"
    },
    uz: {
        page_title: "Trimvert - Universal Media Vositasi",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ platformadan media yuklab oling, kesing va o'zgartiring",
        dark_mode: "Qorong'u Rejim",
        light_mode: "Yorug' Rejim",
        language_label: "Til",
        tab_url: "🔗 URL dan",
        tab_trim: "✂️ Faylni Kesish",
        tab_convert: "🔄 Formatni O'zgartirish",
        url_placeholder: "🔗 Sevimli video yoki qo'shiq havolasini bu yerga joylashtiring...",
        search_btn: "🔍 Qidirish"
    },
    kk: {
        page_title: "Trimvert - Әмбебап Медиа Құралы",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ платформадан медиа жүктеп алыңыз, қиыңыз және түрлендіріңіз",
        dark_mode: "Қараңғы Режим",
        light_mode: "Жарық Режим",
        language_label: "Тіл",
        tab_url: "🔗 URL-ден",
        tab_trim: "✂️ Файлды Қию",
        tab_convert: "🔄 Форматты Түрлендіру",
        url_placeholder: "🔗 Сүйікті бейне немесе әнінің сілтемесін мұнда қойыңыз...",
        search_btn: "🔍 Іздеу"
    },
    ky: {
        page_title: "Trimvert - Универсалдуу Медиа Куралы",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ платформадан медиа жүктөп алыңыз, кесип жана өзгөртүңүз",
        dark_mode: "Караңгы Режим",
        light_mode: "Жарык Режим",
        language_label: "Тил",
        tab_url: "🔗 URL дан",
        tab_trim: "✂️ Файлды Кесүү",
        tab_convert: "🔄 Форматты Өзгөртүү",
        url_placeholder: "🔗 Сүйүктүү видео же ырыңыздын шилтемесин бул жерге коюңуз...",
        search_btn: "🔍 Издөө"
    },
    tg: {
        page_title: "Trimvert - Асбоби Умумии Медиа",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Медиаро аз 1000+ платформа боргирӣ, бурриш ва табдил диҳед",
        dark_mode: "Реҷаи Торик",
        light_mode: "Реҷаи Равшан",
        language_label: "Забон",
        tab_url: "🔗 Аз URL",
        tab_trim: "✂️ Файлро Бурридан",
        tab_convert: "🔄 Форматро Табдил Додан",
        url_placeholder: "🔗 Пайванди видео ё суруди дӯстдоштаатонро дар ин ҷо гузоред...",
        search_btn: "🔍 Ҷустуҷӯ"
    },
    tk: {
        page_title: "Trimvert - Ählumumy Media Guraly",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ platformadan media göçürip alyň, kesiň we öwüriň",
        dark_mode: "Garaňky Režim",
        light_mode: "Ýagtylyk Režim",
        language_label: "Dil",
        tab_url: "🔗 URL-den",
        tab_trim: "✂️ Faýly Kesmek",
        tab_convert: "🔄 Formaty Öwürmek",
        url_placeholder: "🔗 Halanýan wideo ýa-da aýdymyňyzyň baglanyşygyny bu ýere goýuň...",
        search_btn: "🔍 Gözle"
    },
    mn: {
        page_title: "Trimvert - Универсал Медиа Хэрэгсэл",
        main_title: "✨ Trimvert",
        subtitle: "🎬 1000+ платформоос медиа татаж авах, таслах, хувиргах",
        dark_mode: "Харанхуй Горим",
        light_mode: "Гэрэл Горим",
        language_label: "Хэл",
        tab_url: "🔗 URL-аас",
        tab_trim: "✂️ Файл Таслах",
        tab_convert: "🔄 Формат Хувиргах",
        url_placeholder: "🔗 Дуртай видео эсвэл дууныхаа холбоосыг энд буулгана уу...",
        search_btn: "🔍 Хайх"
    },
    ka: {
        page_title: "Trimvert - უნივერსალური მედია ინსტრუმენტი",
        main_title: "✨ Trimvert",
        subtitle: "🎬 ჩამოტვირთეთ, მოჭერით და გარდაქმენით მედია 1000+ პლატფორმიდან",
        dark_mode: "ბნელი რეჟიმი",
        light_mode: "ნათელი რეჟიმი",
        language_label: "ენა",
        tab_url: "🔗 URL-დან",
        tab_trim: "✂️ ფაილის მოჭრა",
        tab_convert: "🔄 ფორმატის გარდაქმნა",
        url_placeholder: "🔗 ჩასვით თქვენი საყვარელი ვიდეოს ან სიმღერის ბმული აქ...",
        search_btn: "🔍 ძიება"
    },
    hy: {
        page_title: "Trimvert - Համընդհանուր Մեդիա Գործիք",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Ներբեռնեք, կտրեք և փոխարկեք մեդիան 1000+ հարթակներից",
        dark_mode: "Մութ Ռեժիմ",
        light_mode: "Լուսավոր Ռեժիմ",
        language_label: "Լեզու",
        tab_url: "🔗 URL-ից",
        tab_trim: "✂️ Ֆայլի Կտրում",
        tab_convert: "🔄 Ֆորմատի Փոխարկում",
        url_placeholder: "🔗 Տեղադրեք ձեր սիրելի տեսանյութի կամ երգի հղումը այստեղ...",
        search_btn: "🔍 Որոնել"
    },
    mt: {
        page_title: "Trimvert - Għodda Universali tal-Medja",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Niżżel, aqta' u kkonverti l-midja minn aktar minn 1000 pjattaforma",
        dark_mode: "Modalità Skura",
        light_mode: "Modalità Ċara",
        language_label: "Lingwa",
        tab_url: "🔗 Minn URL",
        tab_trim: "✂️ Aqta' Fajl",
        tab_convert: "🔄 Ikkonverti Formatt",
        url_placeholder: "🔗 Waħħal il-link tal-video jew il-kanzunetta favorita tiegħek hawn...",
        search_btn: "🔍 Fittex"
    },
    lb: {
        page_title: "Trimvert - Universell Medien Tool",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Lued erof, schneid an konvertéier Medien vun iwwer 1000 Plattformen",
        dark_mode: "Donkel Modus",
        light_mode: "Hell Modus",
        language_label: "Sprooch",
        tab_url: "🔗 Vun URL",
        tab_trim: "✂️ Fichier Schneiden",
        tab_convert: "🔄 Format Konvertéieren",
        url_placeholder: "🔗 Kleebt de Link vun Ärem Liiblingsvideo oder Lidd hei...",
        search_btn: "🔍 Sichen"
    },
    tl: {
        page_title: "Trimvert - Unibersal na Media Tool",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Mag-download, mag-trim at mag-convert ng media mula sa 1000+ platforms",
        dark_mode: "Madilim na Mode",
        light_mode: "Maliwanag na Mode",
        language_label: "Wika",
        tab_url: "🔗 Mula sa URL",
        tab_trim: "✂️ I-trim ang File",
        tab_convert: "🔄 I-convert ang Format",
        url_placeholder: "🔗 I-paste ang link ng iyong paboritong video o kanta dito...",
        search_btn: "🔍 Maghanap"
    },
    ceb: {
        page_title: "Trimvert - Unibersal nga Media Tool",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Pag-download, putol ug usba ang media gikan sa 1000+ nga platform",
        dark_mode: "Ngitngit nga Mode",
        light_mode: "Hayag nga Mode",
        language_label: "Pinulongan",
        tab_url: "🔗 Gikan sa URL",
        tab_trim: "✂️ Putla ang File",
        tab_convert: "🔄 Usba ang Format",
        url_placeholder: "🔗 I-paste ang link sa imong paborito nga video o kanta dinhi...",
        search_btn: "🔍 Pangita"
    },
    jv: {
        page_title: "Trimvert - Piranti Media Universal",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Undhuh, potong lan konversi media saka luwih saka 1000 platform",
        dark_mode: "Mode Peteng",
        light_mode: "Mode Padhang",
        language_label: "Basa",
        tab_url: "🔗 Saka URL",
        tab_trim: "✂️ Potong File",
        tab_convert: "🔄 Konversi Format",
        url_placeholder: "🔗 Tempel link video utawa lagu favorit sampeyan ing kene...",
        search_btn: "🔍 Goleki"
    },
    su: {
        page_title: "Trimvert - Alat Média Universal",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Unduh, motong jeung ngarobah média tina leuwih ti 1000 platform",
        dark_mode: "Mode Poék",
        light_mode: "Mode Caang",
        language_label: "Basa",
        tab_url: "🔗 Ti URL",
        tab_trim: "✂️ Motong Koropak",
        tab_convert: "🔄 Ngarobah Format",
        url_placeholder: "🔗 Témpélkeun tautan video atanapi lagu karesep anjeun di dieu...",
        search_btn: "🔍 Milarian"
    },
    mg: {
        page_title: "Trimvert - Fitaovana Haino aman-jery Iraisam-pirenena",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Misintona, manapaka ary manova haino aman-jery avy amin'ny sehatra 1000+",
        dark_mode: "Fomba Maizina",
        light_mode: "Fomba Mazava",
        language_label: "Fiteny",
        tab_url: "🔗 Avy amin'ny URL",
        tab_trim: "✂️ Manapaka Rakitra",
        tab_convert: "🔄 Manova Endrika",
        url_placeholder: "🔗 Apetaho eto ny rohy amin'ny horonan-tsary na hira tianao...",
        search_btn: "🔍 Hitady"
    },
    so: {
        page_title: "Trimvert - Qalab Warbaahinta Guud",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Soo dejiso, jar oo u beddel warbaahinta ka badan 1000 barta-dhig",
        dark_mode: "Hab Madow",
        light_mode: "Hab Iftiimo",
        language_label: "Luuqad",
        tab_url: "🔗 URL ka",
        tab_trim: "✂️ Jar Faylka",
        tab_convert: "🔄 U Beddel Qaabka",
        url_placeholder: "🔗 Halkan ku dheji isku-xidhka muuqaalka ama heesta aad jeceshahay...",
        search_btn: "🔍 Raadi"
    },
    yi: {
        page_title: "Trimvert - אוניווערסאַל מעדיאַ געצייַג",
        main_title: "✨ Trimvert",
        subtitle: "🎬 אראפקאפיע, שנייַד און קאָנווערטירן מעדיע פון 1000+ פּלאַטפאָרמס",
        dark_mode: "טונקל מאָדע",
        light_mode: "ליכטיק מאָדע",
        language_label: "שפּראַך",
        tab_url: "🔗 פון URL",
        tab_trim: "✂️ שנייַדן טעקע",
        tab_convert: "🔄 קאָנווערטירן פֿאָרמאַט",
        url_placeholder: "🔗 אריינקלעפן דעם לינק פון דיין באַליבסטן ווידעא אָדער ליד דאָ...",
        search_btn: "🔍 זוכן"
    },
    la: {
        page_title: "Trimvert - Instrumentum Media Universale",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Depone, seca et converte media ex plus quam 1000 suggestis",
        dark_mode: "Modus Obscurus",
        light_mode: "Modus Lucidus",
        language_label: "Lingua",
        tab_url: "🔗 Ex URL",
        tab_trim: "✂️ Secare Limam",
        tab_convert: "🔄 Convertere Formam",
        url_placeholder: "🔗 Hic insere vinculum tui video vel carminis dilecti...",
        search_btn: "🔍 Quaerere"
    },
    eo: {
        page_title: "Trimvert - Universala Amaskomunikila Ilo",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Elŝutu, tondu kaj konvertu amaskomunikilojn de pli ol 1000 platformoj",
        dark_mode: "Malhela Reĝimo",
        light_mode: "Hela Reĝimo",
        language_label: "Lingvo",
        tab_url: "🔗 De URL",
        tab_trim: "✂️ Tondi Dosieron",
        tab_convert: "🔄 Konverti Formaton",
        url_placeholder: "🔗 Algluu la ligilon de via preferata video aŭ kanto ĉi tie...",
        search_btn: "🔍 Serĉi"
    },
    ht: {
        page_title: "Trimvert - Zouti Medya Inivèsèl",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Telechaje, koupe epi konvèti medya nan plis pase 1000 platfòm",
        dark_mode: "Mòd Fènwa",
        light_mode: "Mòd Klere",
        language_label: "Lang",
        tab_url: "🔗 Soti nan URL",
        tab_trim: "✂️ Koupe Fichye",
        tab_convert: "🔄 Konvèti Fòma",
        url_placeholder: "🔗 Kole lyen videyo oswa chante prefere w la isit la...",
        search_btn: "🔍 Chèche"
    },
    hmn: {
        page_title: "Trimvert - Universal Media Cuab Yeej",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Rub tawm, txiav thiab hloov xov xwm los ntawm 1000+ platforms",
        dark_mode: "Tsaus Hom",
        light_mode: "Teeb Hom",
        language_label: "Lus",
        tab_url: "🔗 Los ntawm URL",
        tab_trim: "✂️ Txiav Cov Ntaub Ntawv",
        tab_convert: "🔄 Hloov Hom",
        url_placeholder: "🔗 Muab koj cov yeeb yaj kiab lossis nkauj nyiam txuas rau ntawm no...",
        search_btn: "🔍 Tshawb Nrhiav"
    },
    ny: {
        page_title: "Trimvert - Chida cha Media Chapadziko Lonse",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Tsitsani, dulani ndi sinthani media kuchokera pa nsanja zopitilira 1000",
        dark_mode: "Mawonekedwe Akuda",
        light_mode: "Mawonekedwe Owala",
        language_label: "Chilankhulo",
        tab_url: "🔗 Kuchokera ku URL",
        tab_trim: "✂️ Dula Fayilo",
        tab_convert: "🔄 Sinthani Mawonekedwe",
        url_placeholder: "🔗 Ikani ulalo wa kanema kapena nyimbo yanu yomwe mumakonda pano...",
        search_btn: "🔍 Fufuzani"
    },
    sn: {
        page_title: "Trimvert - Chishandiso cheMedia chepasirese",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Dhawuniroudza, cheka uye shandura media kubva kumapuratifomu anopfuura 1000",
        dark_mode: "Modhi Yerima",
        light_mode: "Modhi Yechiedza",
        language_label: "Mutauro",
        tab_url: "🔗 Kubva ku URL",
        tab_trim: "✂️ Cheka Faira",
        tab_convert: "🔄 Shandura Fomati",
        url_placeholder: "🔗 Isa link yevhidhiyo kana rwiyo rwako urwu unofarira pano...",
        search_btn: "🔍 Tsvaga"
    },
    st: {
        page_title: "Trimvert - Sesebelisoa sa Media sa Lefatshe",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Jarolla, khaola le fetola media ho tswa mekhahlelong e fetang 1000",
        dark_mode: "Mokhoa o Lefifi",
        light_mode: "Mokhoa o Khanyang",
        language_label: "Puo",
        tab_url: "🔗 Ho tswa ho URL",
        tab_trim: "✂️ Khaola Faele",
        tab_convert: "🔄 Fetola Mokhoa",
        url_placeholder: "🔗 Beha sehokelo sa video kapa pina eo u e ratang mona...",
        search_btn: "🔍 Batla"
    },
    gd: {
        page_title: "Trimvert - Inneal Meadhanan Uile-choitcheann",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Luchdaich sìos, geàrr agus tionndaidh meadhanan bho còrr air 1000 àrd-ùrlar",
        dark_mode: "Modh Dorcha",
        light_mode: "Modh Soilleir",
        language_label: "Cànan",
        tab_url: "🔗 Bho URL",
        tab_trim: "✂️ Geàrr Faidhle",
        tab_convert: "🔄 Tionndaidh Cruth",
        url_placeholder: "🔗 Cuir an ceangal air a' bhidio no an t-òran as fheàrr leat an seo...",
        search_btn: "🔍 Lorg"
    },
    co: {
        page_title: "Trimvert - Strumentu Media Universale",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Scaricate, tagliate è cunvertite media da più di 1000 piattaforme",
        dark_mode: "Modu Scuru",
        light_mode: "Modu Chjaru",
        language_label: "Lingua",
        tab_url: "🔗 Da URL",
        tab_trim: "✂️ Taglià u Schedariu",
        tab_convert: "🔄 Cunvertisce u Formatu",
        url_placeholder: "🔗 Incollate u ligame di u vostru video o canzona preferita quì...",
        search_btn: "🔍 Circà"
    },
    fy: {
        page_title: "Trimvert - Universeel Media-ark",
        main_title: "✨ Trimvert",
        subtitle: "🎬 Download, knip en konvertearje media fan mear as 1000 platfoarms",
        dark_mode: "Tsjuster Modus",
        light_mode: "Ljocht Modus",
        language_label: "Taal",
        tab_url: "🔗 Fan URL",
        tab_trim: "✂️ Trimbêst",
        tab_convert: "🔄 Konvertearje Formaat",
        url_placeholder: "🔗 Plak de keppeling fan jo favorite fideo of nûmer hjir...",
        search_btn: "🔍 Sykje"
    }
};

// Detectar idioma del navegador
function detectBrowserLanguage() {
    const browserLang = navigator.language || navigator.userLanguage;
    const langCode = browserLang.split('-')[0]; // 'en-US' -> 'en'
    
    // Si el idioma está disponible, usarlo; sino, usar inglés por defecto
    return translations[langCode] ? langCode : 'en';
}

// Obtener idioma guardado o detectar
function getCurrentLanguage() {
    return localStorage.getItem('preferredLanguage') || detectBrowserLanguage();
}

// Cambiar idioma
function changeLanguage(lang) {
    if (!translations[lang]) {
        console.error('Language not supported:', lang);
        return;
    }
    
    localStorage.setItem('preferredLanguage', lang);
    document.documentElement.lang = lang;
    applyTranslations(lang);
    updateCurrentLanguageIndicator();
    toggleSettingsMenu(); // Cerrar el menú
    showNotification('✅ Idioma cambiado', 'success');
}

// Aplicar traducciones a la página
function applyTranslations(lang) {
    const translation = translations[lang];
    
    // Traducir elementos con data-i18n
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translation[key]) {
            if (element.tagName === 'INPUT' && element.type === 'text') {
                element.placeholder = translation[key];
            } else {
                element.textContent = translation[key];
            }
        }
    });
    
    // Actualizar título de la página
    document.title = translation.page_title;
}

// Toggle menú de configuración
function toggleSettingsMenu() {
    const menu = document.getElementById('settingsMenu');
    if (menu) {
        menu.classList.toggle('hidden');
    }
}

// Toggle tema (oscuro/claro)
function toggleTheme() {
    const body = document.body;
    const isDark = !body.classList.contains('light-mode');
    const currentLang = getCurrentLanguage();
    const translation = translations[currentLang];
    
    if (isDark) {
        // Cambiar a modo claro
        body.classList.add('light-mode');
        localStorage.setItem('theme', 'light');
        document.getElementById('themeIcon').textContent = '☀️';
        document.getElementById('themeText').textContent = translation.light_mode || 'Modo Claro';
        document.getElementById('themeValue').textContent = 'ON';
    } else {
        // Cambiar a modo oscuro
        body.classList.remove('light-mode');
        localStorage.setItem('theme', 'dark');
        document.getElementById('themeIcon').textContent = '🌙';
        document.getElementById('themeText').textContent = translation.dark_mode || 'Modo Oscuro';
        document.getElementById('themeValue').textContent = 'ON';
    }
}

// Cargar tema guardado
function loadSavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        document.getElementById('themeIcon').textContent = '☀️';
        const currentLang = getCurrentLanguage();
        const translation = translations[currentLang];
        document.getElementById('themeText').textContent = translation.light_mode || 'Modo Claro';
    }
}

// Cerrar menú al hacer clic fuera
document.addEventListener('click', function(event) {
    const menu = document.getElementById('settingsMenu');
    const settingsBtn = document.querySelector('.settings-btn');
    
    if (menu && !menu.contains(event.target) && event.target !== settingsBtn) {
        menu.classList.add('hidden');
    }
});

// Inicializar idioma y tema al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    const currentLang = getCurrentLanguage();
    applyTranslations(currentLang);
    loadSavedTheme();
    console.log('Language initialized:', currentLang);
    
    // ✨ DETALLES CREATIVOS ✨
    
    // Indicador de progreso de scroll
    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        document.documentElement.style.setProperty('--scroll-progress', scrolled + '%');
    });
    
    // Easter egg: Konami Code (↑ ↑ ↓ ↓ ← → ← → B A)
    let konamiCode = [];
    const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    
    document.addEventListener('keydown', (e) => {
        konamiCode.push(e.key);
        konamiCode = konamiCode.slice(-10);
        
        if (konamiCode.join('') === konamiSequence.join('')) {
            document.body.style.animation = 'rainbow 3s linear infinite';
            const style = document.createElement('style');
            style.textContent = `@keyframes rainbow { 0%, 100% { filter: hue-rotate(0deg); } 50% { filter: hue-rotate(360deg); } }`;
            document.head.appendChild(style);
            
            setTimeout(() => {
                document.body.style.animation = '';
            }, 3000);
        }
    });
    
    // Partículas al hacer click
    document.addEventListener('click', (e) => {
        if (Math.random() > 0.7) { // 30% de probabilidad
            createSparkle(e.clientX, e.clientY);
        }
    });
    
    function createSparkle(x, y) {
        const sparkle = document.createElement('div');
        sparkle.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            width: 10px;
            height: 10px;
            background: radial-gradient(circle, rgba(99,102,241,0.8), transparent);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            animation: sparkleOut 0.6s ease-out forwards;
        `;
        
        const sparkleStyle = document.createElement('style');
        sparkleStyle.textContent = `
            @keyframes sparkleOut {
                0% { transform: scale(0) translateY(0); opacity: 1; }
                100% { transform: scale(2) translateY(-30px); opacity: 0; }
            }
        `;
        
        if (!document.getElementById('sparkle-style')) {
            sparkleStyle.id = 'sparkle-style';
            document.head.appendChild(sparkleStyle);
        }
        
        document.body.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 600);
    }
    
    // ========== NUEVAS FUNCIONALIDADES UX ==========
    
    // Agregar indicadores a todos los idiomas automáticamente
    document.querySelectorAll('.language-option-simple').forEach(option => {
        const langCode = option.getAttribute('onclick').match(/'([^']+)'/)[1];
        if (!option.querySelector('.current-lang-indicator')) {
            const indicator = document.createElement('span');
            indicator.className = 'current-lang-indicator';
            indicator.dataset.lang = langCode;
            indicator.textContent = '✓';
            option.appendChild(indicator);
        }
    });
    
    // Marcar idioma actual
    updateCurrentLanguageIndicator();
    
    // Mostrar hint de shortcuts al inicio (solo primera vez)
    if (!localStorage.getItem('shortcuts-seen')) {
        setTimeout(() => {
            const hint = document.getElementById('shortcutsHint');
            if (hint) {
                hint.classList.add('show');
                setTimeout(() => hint.classList.remove('show'), 5000);
                localStorage.setItem('shortcuts-seen', 'true');
            }
        }, 2000);
    }
    
    // Scroll to top button
    window.addEventListener('scroll', () => {
        const scrollBtn = document.getElementById('scrollTopBtn');
        if (scrollBtn) {
            if (window.scrollY > 100) {
                scrollBtn.classList.add('visible');
            } else {
                scrollBtn.classList.remove('visible');
            }
        }
    });
    
    // Cargar estado del panel de atajos
    const shortcutsCollapsed = localStorage.getItem('shortcuts-collapsed');
    const shortcutsHint = document.getElementById('shortcutsHint');
    if (shortcutsHint && shortcutsCollapsed === 'false') {
        // Si el usuario lo dejó expandido, mantenerlo así
        shortcutsHint.classList.remove('collapsed');
    }

});

// ========== FUNCIONES DE UX ADICIONALES ==========

// Filtrar idiomas en el buscador
function filterLanguages(search) {
    const searchLower = search.toLowerCase();
    const options = document.querySelectorAll('.language-option-simple');
    let visibleCount = 0;
    
    options.forEach(option => {
        const text = option.textContent.toLowerCase();
        if (text.includes(searchLower)) {
            option.style.display = 'flex';
            visibleCount++;
        } else {
            option.style.display = 'none';
        }
    });
    
    // Animación sutil en los resultados
    if (visibleCount === 0) {
        const optionsContainer = document.getElementById('languageOptions');
        if (optionsContainer && !document.getElementById('no-results-msg')) {
            const noResults = document.createElement('div');
            noResults.id = 'no-results-msg';
            noResults.style.cssText = 'padding: 20px; text-align: center; color: var(--text-muted); font-style: italic;';
            noResults.textContent = '😕 No se encontraron idiomas';
            optionsContainer.appendChild(noResults);
        }
    } else {
        const noResultsMsg = document.getElementById('no-results-msg');
        if (noResultsMsg) noResultsMsg.remove();
    }
}

// Actualizar indicador de idioma actual
function updateCurrentLanguageIndicator() {
    const currentLang = getCurrentLanguage();
    document.querySelectorAll('.current-lang-indicator').forEach(indicator => {
        indicator.classList.remove('active');
        if (indicator.dataset.lang === currentLang) {
            indicator.classList.add('active');
        }
    });
}

// Scroll suave hacia arriba
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Toggle shortcuts panel
function toggleShortcuts() {
    const shortcutsHint = document.getElementById('shortcutsHint');
    if (shortcutsHint) {
        const isCollapsed = shortcutsHint.classList.toggle('collapsed');
        
        // Guardar estado en localStorage
        localStorage.setItem('shortcuts-collapsed', isCollapsed);
    }
}

// Pegar desde portapapeles
async function pasteFromClipboard() {
    try {
        const text = await navigator.clipboard.readText();
        const urlInput = document.querySelector('input[type="text"][placeholder*="URL"], input[type="text"][placeholder*="url"], input[type="text"][placeholder*="link"]');
        
        if (urlInput && text) {
            urlInput.value = text;
            urlInput.focus();
            
            // Animación de feedback
            urlInput.style.animation = 'flashGreen 0.5s ease';
            setTimeout(() => urlInput.style.animation = '', 500);
            
            // Agregar animación si no existe
            if (!document.getElementById('flash-green-style')) {
                const style = document.createElement('style');
                style.id = 'flash-green-style';
                style.textContent = `
                    @keyframes flashGreen {
                        0%, 100% { box-shadow: 0 5px 25px rgba(99, 102, 241, 0.3); }
                        50% { box-shadow: 0 5px 25px rgba(16, 185, 129, 0.6), 0 0 0 3px rgba(16, 185, 129, 0.2); }
                    }
                `;
                document.head.appendChild(style);
            }
            
            // Mostrar notificación
            showNotification('✅ URL pegada desde portapapeles', 'success');
        }
    } catch (err) {
        showNotification('⚠️ No se pudo acceder al portapapeles', 'warning');
    }
}

// Modo Teatro
function toggleTheaterMode() {
    document.body.classList.toggle('theater-mode');
    const btn = document.getElementById('theaterBtn');
    btn.classList.toggle('active');
    
    if (document.body.classList.contains('theater-mode')) {
        showNotification('🎬 Modo Teatro activado (Presiona F o Esc para salir)', 'info');
        // Scroll suave al contenido principal
        setTimeout(() => {
            const main = document.querySelector('main');
            if (main) main.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    } else {
        document.body.classList.remove('theater-focus');
        showNotification('✨ Modo normal activado', 'info');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Pantalla completa en modo teatro
function toggleTheaterFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().then(() => {
            showNotification('⛶ Pantalla completa activada (F11 o Esc para salir)', 'success');
        }).catch(err => {
            showNotification('⚠️ No se pudo activar pantalla completa', 'warning');
        });
    } else {
        document.exitFullscreen().then(() => {
            showNotification('✓ Pantalla completa desactivada', 'info');
        });
    }
}

// Modo enfoque (oculta controles)
function toggleTheaterFocus() {
    document.body.classList.toggle('theater-focus');
    const focusText = document.getElementById('focusText');
    
    if (document.body.classList.contains('theater-focus')) {
        focusText.textContent = 'Desenfocar';
        showNotification('🎯 Modo enfoque: controles ocultos (Presiona F de nuevo)', 'info');
    } else {
        focusText.textContent = 'Enfocar';
        showNotification('👁️ Controles visibles', 'info');
    }
}

// Sistema de notificaciones
function showNotification(message, type = 'info') {
    const existingNotif = document.querySelector('.custom-notification');
    if (existingNotif) existingNotif.remove();
    
    const notif = document.createElement('div');
    notif.className = 'custom-notification';
    notif.textContent = message;
    
    const colors = {
        success: 'rgba(16, 185, 129, 0.95)',
        warning: 'rgba(245, 158, 11, 0.95)',
        error: 'rgba(239, 68, 68, 0.95)',
        info: 'rgba(99, 102, 241, 0.95)'
    };
    
    notif.style.cssText = `
        position: fixed;
        top: 80px;
        right: 30px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        font-weight: 600;
        font-size: 0.95rem;
        animation: slideInRight 0.4s ease, slideOutRight 0.4s ease 2.6s forwards;
        backdrop-filter: blur(10px);
    `;
    
    if (!document.getElementById('notif-style')) {
        const style = document.createElement('style');
        style.id = 'notif-style';
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(400px); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(400px); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notif);
    setTimeout(() => notif.remove(), 3000);
}

// Atajos de teclado globales
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + V - Pegar desde portapapeles
    if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        const activeElement = document.activeElement;
        if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            pasteFromClipboard();
        }
    }
    
    // F - Modo Teatro
    if (e.key === 'f' || e.key === 'F') {
        const activeElement = document.activeElement;
        if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            toggleTheaterMode();
        }
    }
    
    // Esc - Salir de modo teatro o cerrar menús
    if (e.key === 'Escape') {
        if (document.body.classList.contains('theater-mode')) {
            toggleTheaterMode();
        }
        const settingsMenu = document.getElementById('settingsMenu');
        if (settingsMenu) settingsMenu.classList.add('hidden');
        
        // Salir de pantalla completa
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
    }
    
    // ? - Mostrar ayuda de shortcuts (ahora expande el panel)
    if (e.key === '?') {
        const hint = document.getElementById('shortcutsHint');
        if (hint) {
            // Expandir el panel si está colapsado
            if (hint.classList.contains('collapsed')) {
                hint.classList.remove('collapsed');
                localStorage.setItem('shortcuts-collapsed', false);
                showNotification('Atajos de teclado mostrados', 'info');
            }
        }
    }
    
    // T - Toggle modo enfoque en teatro
    if ((e.key === 't' || e.key === 'T') && document.body.classList.contains('theater-mode')) {
        const activeElement = document.activeElement;
        if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
            e.preventDefault();
            toggleTheaterFocus();
        }
    }
    
    // F11 - Pantalla completa (interceptar para mostrar notificación)
    if (e.key === 'F11') {
        e.preventDefault();
        toggleTheaterFullscreen();
    }
    
    // Enter - Buscar (si hay input enfocado con URL)
    if (e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.type === 'text' && activeElement.value.includes('http')) {
            const searchBtn = document.querySelector('button[onclick*="searchMedia"]');
            if (searchBtn) searchBtn.click();
        }
    }
});

// ========== CURSOR HERMOSO ==========
(function() {
    const cursorDot = document.querySelector('.cursor-dot');
    const cursorOutline = document.querySelector('.cursor-outline');
    
    if (!cursorDot || !cursorOutline) return;
    
    let mouseX = 0, mouseY = 0;
    let dotX = 0, dotY = 0;
    let outlineX = 0, outlineY = 0;
    
    // Seguir mouse
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    // Animar cursor suavemente
    function animate() {
        // Punto central - rápido
        dotX += (mouseX - dotX) * 0.4;
        dotY += (mouseY - dotY) * 0.4;
        cursorDot.style.left = dotX + 'px';
        cursorDot.style.top = dotY + 'px';
        
        // Contorno - lento
        outlineX += (mouseX - outlineX) * 0.15;
        outlineY += (mouseY - outlineY) * 0.15;
        cursorOutline.style.left = outlineX - 20 + 'px';
        cursorOutline.style.top = outlineY - 20 + 'px';
        
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // Efecto hover
    const interactiveElements = document.querySelectorAll('a, button, input, textarea, select, .upload-area, .format-option, .language-option-simple, .float-btn, .settings-btn');
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursorDot.classList.add('hover');
            cursorOutline.classList.add('hover');
        });
        
        el.addEventListener('mouseleave', () => {
            cursorDot.classList.remove('hover');
            cursorOutline.classList.remove('hover');
        });
    });
})();

