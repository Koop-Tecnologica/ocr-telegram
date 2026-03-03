import os
import asyncio
from telethon import TelegramClient, events
# No es estrictamente necesario load_dotenv en Render porque ya configuraste las variables en el panel
# pero lo dejamos por si pruebas localmente.

# 1. Configuraciones desde Variables de Entorno de Render
api_id = os.getenv('APP_ID') # En tu Render pusiste APP_ID
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN') # Usaremos el Token del BotFather

# 2. Asegurar carpeta de descargas
CARPETA = 'descargas'
if not os.path.exists(CARPETA):
    os.makedirs(CARPETA)
    print(f"Carpeta '{CARPETA}' creada para Render.")

# 3. Inicializar el cliente como BOT (más estable para servidores)
# Usamos 'bot_session' para que no pida código de verificación por SMS en el servidor
client = TelegramClient('bot_session', api_id, api_hash)

# 4. Escuchar mensajes nuevos con imágenes
@client.on(events.NewMessage)
async def manejador_de_mensajes(event):
    # Si el mensaje tiene una foto
    if event.photo:
        print(f"Detectada imagen en mensaje {event.id}. Descargando...")
        path = await event.download_media(file=CARPETA)
        print(f"¡Imagen guardada en: {path}!")
        
        # Aquí es donde podrías llamar a tu función de OCR de sistema_final.py
        # Ejemplo: procesar_todo() 

    # Responder al usuario para saber que está vivo
    if event.text == '/start':
        await event.respond("¡Hola! Soy tu bot de OCR en Render. Envíame una imagen.")

async def main():
    print("Bot conectado y esperando imágenes...")
    # Iniciamos sesión usando el BOT_TOKEN de las variables de entorno
    await client.start(bot_token=bot_token)
    # Esto mantiene al bot encendido indefinidamente en Render
    await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())