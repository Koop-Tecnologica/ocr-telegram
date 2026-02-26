import os
import re
import pandas as pd
import pytesseract
from PIL import Image

# 1. Configuraciones iniciales
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
CARPETA_FOTOS = 'descargas/'
ARCHIVO_EXCEL = 'Reporte_Extraccion_Diana.xlsx'

def procesar_todo():
    datos_finales = []
    print("--- INICIANDO PROCESAMIENTO INTEGRAL ---")

    # 2. Listar las imágenes descargadas de Telegram
    imagenes = [f for f in os.listdir(CARPETA_FOTOS) if f.endswith(('.jpg', '.png'))]
    
    for nombre in imagenes:
        ruta = os.path.join(CARPETA_FOTOS, nombre)
        print(f"Leyendo: {nombre}...")
        
        # 3. Aplicar OCR
        texto = pytesseract.image_to_string(Image.open(ruta), lang='spa')
        
        # 4. Extraer datos con la "inteligencia" del Día 4 (Regex)
        email = re.findall(r'[a-zA-Z0-9._-]+\.edu\.co|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
        cargo = re.findall(r'PSICÓLOGO\s?\(?[A-Z]?\)?', texto, re.IGNORECASE)
        
        # 5. Organizar en un diccionario
        datos_finales.append({
            "Fecha": "2026-02-13", # Podrías usar la fecha actual
            "Entidad": "Detectada por OCR", 
            "Cargo": cargo[0] if cargo else "No identificado",
            "Contacto": email[0] if email else "No encontrado",
            "Imagen_Origen": nombre
        })

    # 6. Guardar en Excel usando Pandas
    df = pd.DataFrame(datos_finales)
    df.to_excel(ARCHIVO_EXCEL, index=False)
    print(f"\n✅ PROCESO TERMINADO. Revisa tu archivo: {ARCHIVO_EXCEL}")

if __name__ == "__main__":
    procesar_todo()