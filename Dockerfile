FROM python:3.10-slim

# 1. Instalamos Tesseract OCR y dependencias del sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean

# 2. Establecemos el directorio de trabajo
WORKDIR /app

# 3. Copiamos todos los archivos del repositorio al contenedor
COPY . .

# 4. Creamos la carpeta de descargas
RUN mkdir -p descargas

# 5. Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Lanzamiento del servicio
CMD python conexion_telegram.py & python -m http.server $PORT