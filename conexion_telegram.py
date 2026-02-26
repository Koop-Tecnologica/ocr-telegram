import os
from telethon import TelegramClient

# Credenciales (verificadas y listas)
api_id = '33548315'
api_hash = 'e49a33cf6a585f9e66e0b2097b24676c'
nombre_sesion = 'sesion_diana'

# Creamos la carpeta de descargas automáticamente si no existe
# Esto evita el error de "Folder not found"
if not os.path.exists('descargas'):
    os.makedirs('descargas')
    print("Carpeta 'descargas' creada exitosamente.")

# Creamos el cliente de Telegram
client = TelegramClient(nombre_sesion, api_id, api_hash)

async def main():
    print("Conectando al sistema de Telegram...")
    
    # Usamos un canal verificado para evitar errores de nombre
    try:
        async for message in client.iter_messages('me', limit=10):
            # Limpiamos el texto para evitar errores si el mensaje es None
            texto = message.text[:50].replace('\n', ' ') if message.text else "Sin texto"
            print(f"ID: {message.id} | Texto: {texto}...")
            
            # Verificamos si el mensaje tiene contenido multimedia (foto)
            if message.photo:
                print(f"Descargando imagen del mensaje {message.id}...")
                path = await message.download_media(file='descargas/')
                print(f"¡Imagen guardada en: {path}!")
    except Exception as e:
        print(f"Ocurrió un error durante la extracción: {e}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())