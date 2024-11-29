import requests
import os
from PIL import Image

def create_full_mask(image_path, mask_path):
    """
    Crea una máscara completamente negra que cubre toda la imagen.
    
    Args:
        image_path (str): Ruta a la imagen original.
        mask_path (str): Ruta donde se guardará la máscara creada.
    """
    with Image.open(image_path) as img:
        mask = Image.new("L", img.size, 0)  # Máscara negra
        mask.save(mask_path)
    print(f"Máscara creada y guardada en: {mask_path}")

def validate_mask(image_path, mask_path):
    """
    Valida que la máscara tenga el mismo tamaño que la imagen original.
    
    Args:
        image_path (str): Ruta a la imagen original.
        mask_path (str): Ruta a la máscara creada.
    
    Returns:
        bool: Verdadero si la máscara es válida, falso de lo contrario.
    """
    with Image.open(image_path) as img:
        with Image.open(mask_path) as mask:
            return img.size == mask.size

def download_image(url, save_path):
    """
    Descarga una imagen desde una URL y la guarda localmente.
    
    Args:
        url (str): URL de la imagen.
        save_path (str): Ruta donde se guardará la imagen descargada.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen descargada: {save_path}")
    else:
        raise Exception(f"Error al descargar la imagen: {response.status_code}")

def delete_file(file_path):
    """
    Elimina un archivo si existe.
    
    Args:
        file_path (str): Ruta al archivo que se desea eliminar.
    """
    try:
        os.remove(file_path)
        print(f"Archivo eliminado: {file_path}")
    except OSError as e:
        print(f"No se pudo eliminar el archivo {file_path}: {e}")

def edit_image(arguments, context):
    """
    Realiza la edición de una imagen utilizando la API de Ideogram.
    
    Args:
        arguments (dict): Diccionario con los parámetros para la edición.
        context (dict): Contexto compartido para almacenar la URL de la imagen editada.
    
    Returns:
        dict: Respuesta de la API en formato JSON.
    """
    api_key = os.getenv("IDEOGRAM_API_KEY")
    if not api_key:
        raise Exception("La clave de API 'IDEOGRAM_API_KEY' no está configurada.")

    url = "https://api.ideogram.ai/edit"
    headers = {"Api-Key": api_key}

    # Obtener la URL de la imagen desde los argumentos o el contexto
    image_url = arguments.get("image_url") or context.get("last_generated_image_url")
    if not image_url:
        print("No se proporcionó 'image_url' y no hay una URL de imagen previa.")
        return {"error": "No se proporcionó 'image_url' y no hay una URL de imagen previa."}

    # Rutas de archivos temporales
    temp_image_path = "temp_image.jpg"
    temp_mask_path = "temp_mask.png"

    try:
        # Descargar la imagen desde la URL
        print(f"Descargando la imagen desde la URL: {image_url}")
        download_image(image_url, temp_image_path)

        # Crear una máscara completa
        print("Creando la máscara para la edición...")
        create_full_mask(temp_image_path, temp_mask_path)

        # Validar la máscara
        if not validate_mask(temp_image_path, temp_mask_path):
            raise Exception("La máscara no coincide con el tamaño de la imagen original.")
        print("La máscara es válida y coincide con la imagen.")

        # Preparar la solicitud a la API
        print("Preparando los datos para la edición...")
        files = {
            "image_file": open(temp_image_path, "rb"),
            "mask": open(temp_mask_path, "rb"),
        }

        payload = {
            "prompt": arguments["prompt"],
            "style_type": arguments.get("style_type", "REALISTIC"),
        }

        optional_fields = [
            "magic_prompt_option",
            "seed",
        ]

        for field in optional_fields:
            if field in arguments and arguments[field] is not None:
                payload[field] = arguments[field]

        response = requests.post(url, data=payload, files=files, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error en la API: {response.status_code} - {response.text}")

        # Procesar la respuesta
        response_data = response.json()
        edited_url = response_data.get("data", [{}])[0].get("url")

        if edited_url:
            context["last_generated_image_url"] = edited_url
            print(f"\nURL de la imagen editada: {edited_url}\n")
        else:
            print("\nNo se pudo obtener la URL de la imagen editada.")
            edited_url = "No disponible"

        return {"url": edited_url}

    finally:
        # Eliminar archivos temporales
        delete_file(temp_image_path)
        delete_file(temp_mask_path)
