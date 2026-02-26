import re

# El texto que el OCR sacó ayer (lo usamos de prueba)
texto_ocr = """
SANTOTOMÁS
TE ESTAMOS gSUscCANDO
PSICÓLOGO (A)
hojadevidaustavillavicencio.edu.co
USTAVILLAVICENCIO.EDU.CO
"""

def extraer_informacion(texto):
    print("--- BUSCANDO DATOS ESTRUCTURADOS ---")
    
    # 1. Buscar Emails (ajustado para detectar el de la Santo Tomás aunque le falte el @)
    # Buscamos patrones que tengan '.edu.co' o '.com'
    patron_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(patron_email, texto)
    
    # Truco extra: Si no hay @ pero hay .edu.co, lo tomamos como posible contacto
    if not emails:
        emails = re.findall(r'[a-zA-Z0-9._-]+\.edu\.co', texto)

    # 2. Buscar Cargos (buscamos palabras en mayúsculas después de 'Buscando' o 'Psicólogo')
    patron_cargo = r'PSICÓLOGO\s?\(?[A-Z]?\)?'
    cargos = re.findall(patron_cargo, texto, re.IGNORECASE)

    print(f"Contactos/Emails encontrados: {emails}")
    print(f"Cargos detectados: {cargos}")
    
    return emails, cargos

if __name__ == "__main__":
    extraer_informacion(texto_ocr)