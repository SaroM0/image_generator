import requests
import os

def remix_image(arguments, context):
    """
    Realiza un remix de una imagen usando la API de Ideogram.

    Args:
        arguments (dict): Diccionario con los parámetros necesarios para el remix.
        context (dict): Contexto compartido para almacenar la URL de la imagen generada.

    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    api_key = os.getenv("IDEOGRAM_API_KEY")
    if not api_key:
        raise Exception("La clave de API 'IDEOGRAM_API_KEY' no está configurada.")

    url = "https://api.ideogram.ai/remix"
    headers = {"Api-Key": api_key}

    # Obtener la URL de la imagen desde los argumentos o el contexto
    image_url = arguments.get("image_url") or context.get("last_generated_image_url")
    if not image_url:
        print("No se proporcionó 'image_url' y no hay una URL de imagen previa.")
        return {"error": "No se proporcionó 'image_url' y no hay una URL de imagen previa."}

    # Descargar la imagen desde la URL
    print(f"Descargando la imagen desde la URL: {image_url}")
    response_image = requests.get(image_url)
    if response_image.status_code != 200:
        raise Exception(f"Error al descargar la imagen: {response_image.status_code} - {response_image.text}")

    # Construir el payload con los campos obligatorios
    payload = {
        "image_request": {
            "prompt": arguments["prompt"],  # Campo obligatorio
        }
    }

    # Añadir campos opcionales si están presentes
    optional_fields = [
        "aspect_ratio",
        "image_weight",
        "magic_prompt_option",
        "model",
        "seed",
        "style_type",
        "negative_prompt",
        "resolution",
        "color_palette",
    ]

    for field in optional_fields:
        if field in arguments and arguments[field] is not None:
            payload["image_request"][field] = arguments[field]

    # Enviar la imagen y el payload a la API
    print("Enviando la imagen a la API para realizar el remix...")
    files = {"image_file": ("image.jpg", response_image.content, "image/jpeg")}
    response = requests.post(url, files=files, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en la API: {response.status_code} - {response.text}")

    # Procesar la respuesta
    response_data = response.json()
    remixed_url = response_data.get("data", [{}])[0].get("url")

    if remixed_url:
        context["last_generated_image_url"] = remixed_url
        print(f"\nURL de la imagen remixada: {remixed_url}\n")
    else:
        print("\nNo se pudo obtener la URL de la imagen remixada.")
        remixed_url = "No disponible"

    return {"url": remixed_url}
