import pytesseract
from PIL import Image

# 1. ESTA ES LA SOLUCIÓN AL ERROR DE TU IMAGEN:
# Le decimos a Python exactamente dónde está instalado Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def realizar_prueba():
    try:
        # 2. Asegúrate de tener una imagen llamada 'test.png' en la misma carpeta que este código
        # Puedes crear una en Paint que diga "Hola Diana"
        nombre_imagen = "test.png" 
        
        imagen = Image.open(nombre_imagen)
        texto = pytesseract.image_to_string(imagen)
        
        print("--- RESULTADO DEL OCR ---")
        print(texto)
        print("-------------------------")
        
    except FileNotFoundError:
        print("Error: No encontré la imagen 'test.png'. Crea una para probar.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    realizar_prueba()