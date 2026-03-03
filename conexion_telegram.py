import os
import asyncio
import re
import pandas as pd
import pytesseract
from PIL import Image
from telethon import TelegramClient, events

# 1. Configuraciones desde las Variables de Env de Render
api_id = os.getenv('APP_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# Configuración de carpetas y archivos
CARPETA = 'descargas'
ARCHIVO_EXCEL = 'Reporte_Extraccion_Diana.xlsx'

if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)
    print(f"Carpeta '{CARPETA}' creada para el servidor.")

# 2. Inicializar el cliente
client = TelegramClient('bot_session', api_id, api_hash)

# 3. Función de procesamiento OCR (Lógica de tu sistema_final.py)
def realizar_ocr(ruta_imagen):
    try:
        # En Render/Linux no se define la ruta de tesseract.exe, se detecta solo
        texto = pytesseract.image_to_string(Image.open(ruta_imagen), lang='spa')
        
        # Extracción con Regex
        email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
        cargo = re.findall(r'PSICÓLOGO\s?\(?[A-Z]?\)?', texto, re.IGNORECASE)
        
        resultado = {
            "Email": email[0] if email else "No encontrado",
            "Cargo": cargo[0] if cargo else "No identificado",
            "Texto_Completo": texto[:100] + "..." # Resumen para el log
        }
        return resultado
    except Exception as e:
        print(f"Error en OCR: {e}")
        return None

# 4. EVENTO: Se activa al recibir una foto
@client.on(events.NewMessage)
async def manejador_de_mensajes(event):
    if event.photo:
        await event.respond("📥 Imagen recibida. Procesando texto, espera un momento...")
        
        # Descargar
        path = await event.download_media(file=CARPETA)
        print(f"Imagen guardada en: {path}")
        
        # Procesar con OCR (usamos run_in_executor para no bloquear el bot)
        loop = asyncio.get_event_loop()
        datos = await loop.run_in_executor(None, realizar_ocr, path)
        
        if datos:
            respuesta = (
                f"✅ **OCR Completado**\n\n"
                f"📧 **Contacto:** {datos['Email']}\n"
                f"💼 **Cargo:** {datos['Cargo']}\n"
            )
            await event.respond(respuesta)
        else:
            await event.respond("❌ No pude procesar la imagen.")

    if event.text == '/start':
        await event.respond("¡Hola! Envíame una imagen de una tarjeta o documento y extraeré los datos por ti.")

# 5. Ejecución principal
async def main():
    print("Conectando bot...")
    await client.start(bot_token=bot_token)
    print("--- BOT EN LÍNEA (RENDER) ---")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())