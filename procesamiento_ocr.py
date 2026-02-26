import pytesseract
from PIL import Image, ImageOps, ImageFilter
import os

# Configuración obligatoria de ruta
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocesar_imagen(ruta_imagen):
    """
    Mejora la imagen para que Tesseract lea mejor.
    """
    with Image.open(ruta_imagen) as img:
        # 1. Convertir a escala de grises
        img = img.convert('L')
        # 2. Aumentar el contraste
        img = ImageOps.autocontrast(img)
        # 3. Aplicar un pequeño filtro de nitidez
        img = img.filter(ImageFilter.SHARPEN)
        
        ruta_pre = ruta_imagen.replace(".", "_pre.")
        img.save(ruta_pre)
        return ruta_pre

def extraer_datos_dia3(carpeta):
    print(f"Iniciando lectura de imágenes en: {carpeta}")
    archivos = [f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta, archivo)
        print(f"\n--- Procesando: {archivo} ---")
        
        # Probamos con preprocesamiento
        ruta_optimizada = preprocesar_imagen(ruta_completa)
        texto = pytesseract.image_to_string(Image.open(ruta_optimizada), lang='spa')
        
        print("Texto Extraído:")
        print(texto.strip())

if __name__ == "__main__":
    # Usamos la carpeta donde descargaste las fotos ayer
    ruta_fotos = 'descargas/' 
    if os.path.exists(ruta_fotos):
        extraer_datos_dia3(ruta_fotos)
    else:
        print("Error: No encontré la carpeta de descargas del Día 2.")