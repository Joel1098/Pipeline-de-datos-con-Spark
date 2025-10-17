import requests
from core.exceptions import ExtractError


def extract_products(api_url):
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx
        print("Extracción de datos exitosa.")
        return response.json()
    except requests.RequestException as e:
        raise ExtractError("Error al extraer datos de la API.", e)
    
    