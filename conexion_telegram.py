import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
nombre_sesion = os.getenv('NOMBRE_SESION')

# Creamos la carpeta de descargas automáticamente si no existe
# Esto evita el error de "Folder not found"
if not os.path.exists('descargas'):
    os.makedirs('descargas')
    print("Carpeta 'descargas' creada exitosamente.")

# Creamos el cliente de Telegram
client = TelegramClient(nombre_sesion, api_id, api_hash)

async def main():
    print("Conectando al sistema de Telegram...")
    
    try:
        async for message in client.iter_messages('me', limit=10):
            texto = message.text[:50].replace('\n', ' ') if message.text else "Sin texto"
            print(f"ID: {message.id} | Texto: {texto}...")
            
            if message.photo:
                print(f"Descargando imagen del mensaje {message.id}...")
                path = await message.download_media(file='descargas/')
                print(f"¡Imagen guardada en: {path}!")
    except Exception as e:
        print(f"Ocurrió un error durante la extracción: {e}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())