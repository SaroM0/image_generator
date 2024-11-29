import requests
import os

def generate_image(arguments, context):
    """
    Genera una imagen utilizando la API de Ideogram.

    Args:
        arguments (dict): Diccionario con los parámetros necesarios para la generación.
        context (dict): Contexto compartido para almacenar la URL de la imagen generada.

    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    api_key = os.getenv("IDEOGRAM_API_KEY")
    if not api_key:
        raise Exception("La clave de API 'IDEOGRAM_API_KEY' no está configurada.")

    url = "https://api.ideogram.ai/generate"
    headers = {"Api-Key": api_key, "Content-Type": "application/json"}

    # Construir el payload con los campos obligatorios
    payload = {
        "image_request": {
            "prompt": arguments["prompt"],  # Campo obligatorio
        }
    }

    # Añadir campos opcionales si están presentes en los argumentos
    optional_fields = [
        "aspect_ratio",
        "model",
        "magic_prompt_option",
        "seed",
        "style_type",
        "negative_prompt",
        "resolution",
        "color_palette",
    ]

    for field in optional_fields:
        if field in arguments and arguments[field] is not None:
            payload["image_request"][field] = arguments[field]

    print("Enviando los siguientes datos a la API para generar la imagen:")
    print(payload)

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en la API: {response.status_code} - {response.text}")

    # Procesar la respuesta
    response_data = response.json()
    generated_url = response_data.get("data", [{}])[0].get("url")

    if generated_url:
        context["last_generated_image_url"] = generated_url
        print(f"\nURL de la imagen generada: {generated_url}\n")
    else:
        print("\nNo se pudo obtener la URL de la imagen generada.")
        generated_url = "No disponible"

    return {"url": generated_url}
