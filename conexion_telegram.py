import os
import asyncio
import re
import pytesseract
from PIL import Image
from telethon import TelegramClient, events
from datetime import datetime

# 1. Configuraciones desde las Variables de Entorno
api_id = os.getenv('APP_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# Configuración de carpetas
CARPETA = 'descargas'
if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)
    print(f"Carpeta '{CARPETA}' creada para el servidor.")

# 2. Inicializar el cliente (Sesión fija para Render)
client = TelegramClient('bot_session', api_id, api_hash)

# 3. Función de procesamiento OCR
def realizar_ocr(ruta_imagen):
    try:
        # En Linux/Render, pytesseract encuentra tesseract automáticamente
        texto = pytesseract.image_to_string(Image.open(ruta_imagen), lang='spa')
        
        # Extracción con Regex mejorada
        email = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
        cargo = re.findall(r'PSICÓLOGO\s?\(?[A-Z]?\)?', texto, re.IGNORECASE)
        
        return {
            "Email": email[0] if email else "No encontrado",
            "Cargo": cargo[0] if cargo else "No identificado",
            "Texto_Completo": texto
        }
    except Exception as e:
        print(f"Error en OCR: {e}")
        return None

# 4. EVENTO: Se activa al recibir una foto
@client.on(events.NewMessage)
async def manejador_de_mensajes(event):
    if event.photo:
        await event.respond("📥 Imagen recibida. Procesando texto...")
        
        # Descargar temporalmente
        path = await event.download_media(file=CARPETA)
        
        # Procesar con OCR
        loop = asyncio.get_event_loop()
        datos = await loop.run_in_executor(None, realizar_ocr, path)
        
        if datos:
            fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")
            respuesta = (
                f"✅ **OCR Completado** ({fecha_hoy})\n\n"
                f"📧 **Contacto:** {datos['Email']}\n"
                f"💼 **Cargo:** {datos['Cargo']}\n"
                f"\n📝 **Extracto:**\n`{datos['Texto_Completo'][:150]}...`"
            )
            await event.respond(respuesta)
        else:
            await event.respond("❌ No pude procesar la imagen.")
        
        # Limpieza: Borrar imagen para ahorrar espacio en Render
        if os.path.exists(path):
            os.remove(path)

    if event.text == '/start':
        await event.respond("¡Hola! Envíame una imagen y extraeré los datos por ti. Estoy activo en Render.")

# 5. Ejecución principal
async def main():
    print("Conectando bot...")
    await client.start(bot_token=bot_token)
    print("--- BOT EN LÍNEA (RENDER) ---")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())