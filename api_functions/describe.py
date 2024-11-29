import requests
import os

def describe_image(arguments, context):
    """
    Describe una imagen usando la API de Ideogram.

    Args:
        arguments (dict): Diccionario con los parámetros necesarios para la descripción.
        context (dict): Contexto compartido con la URL de la última imagen generada.

    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    api_key = os.getenv("IDEOGRAM_API_KEY")
    if not api_key:
        raise Exception("La clave de API 'IDEOGRAM_API_KEY' no está configurada.")

    url = "https://api.ideogram.ai/describe"
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

    # Enviar la imagen a la API
    print("Enviando la imagen a la API para obtener la descripción...")
    files = {"image_file": ("image.jpg", response_image.content, "image/jpeg")}

    response = requests.post(url, files=files, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en la API: {response.status_code} - {response.text}")

    # Procesar la respuesta
    response_data = response.json()
    description = response_data.get("data", [{}])[0].get("description")

    if description:
        print(f"\nDescripción obtenida: {description}\n")
    else:
        print("\nNo se pudo obtener una descripción para la imagen.")
        description = "No disponible"

    return {"description": description}
