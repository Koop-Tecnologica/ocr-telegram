FROM python:3.10-slim

# Instalamos Tesseract OCR y dependencias necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean

WORKDIR /app

# Copiamos los archivos
COPY . .

# Instalamos las librerías de Python
# Asegúrate de tener un archivo requirements.txt con: python-telegram-bot, pytesseract, etc.
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar tu bot
CMD ["python", "sistema_final.py"]