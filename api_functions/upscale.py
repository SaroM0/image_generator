import requests
import os
import json

def upscale_image(arguments, context):
    """
    Realiza un upscale de una imagen usando la API de Ideogram.
    """
    # Obtener la clave de API
    api_key = os.getenv("IDEOGRAM_API_KEY")
    if not api_key:
        raise Exception("La clave de API 'IDEOGRAM_API_KEY' no está configurada.")

    url = "https://api.ideogram.ai/upscale"
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

    # Construir el campo 'image_request'
    image_request = {
        "resemblance": arguments.get("resemblance", 50),  # Valor por defecto 50
        "detail": arguments.get("detail", 50),  # Valor por defecto 50
    }

    # Añadir campos opcionales si están presentes
    optional_fields = [
        "prompt",
        "magic_prompt_option",
        "seed",
    ]
    for field in optional_fields:
        if field in arguments and arguments[field] is not None:
            image_request[field] = arguments[field]

    # Construir el payload
    payload = {
        "image_request": json.dumps(image_request)  # Convertir a JSON
    }

    # Enviar la imagen y el payload a la API
    print("Enviando la imagen a la API para realizar el upscale...")
    files = {"image_file": ("image.jpg", response_image.content, "image/jpeg")}

    response = requests.post(url, data=payload, files=files, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en la API: {response.status_code} - {response.text}")

    # Procesar la respuesta
    response_data = response.json()
    upscaled_url = response_data.get("data", [{}])[0].get("url")

    if upscaled_url:
        context["last_generated_image_url"] = upscaled_url
        print(f"\nURL de la imagen escalada: {upscaled_url}\n")
    else:
        print("\nNo se pudo obtener la URL de la imagen escalada.")
        upscaled_url = "No disponible"

    return {"url": upscaled_url}
