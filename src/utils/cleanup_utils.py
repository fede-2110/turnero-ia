# src/utils/cleanup_utils.py
import re

def clean_dni(dni):
    # Elimina puntos, espacios y otros caracteres no numéricos
    return re.sub(r'\D', '', dni)
