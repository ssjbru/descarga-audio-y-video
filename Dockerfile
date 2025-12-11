# Dockerfile para descarga-audio-y-video con Streamlink + plugins
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . /app

# Instalar dependencias Python
RUN pip install --upgrade pip
RUN pip install --upgrade streamlink
RUN pip install git+https://github.com/streamlink/streamlink-plugins.git
RUN pip install -r requirements.txt

# Exponer el puerto (ajusta si usas otro)
EXPOSE 10000

# Comando para iniciar la app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000", "--workers", "2", "--timeout", "300"]
