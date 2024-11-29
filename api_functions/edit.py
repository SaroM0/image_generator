import requests
import os
from PIL import Image

def create_full_mask(image_path, mask_path, padding=10):
    """
    Crea una máscara completamente blanca más pequeña que la imagen original.
    padding: número de píxeles a reducir en cada lado de la máscara.
    """
    with Image.open(image_path) as img:
        # Reducir las dimensiones de la máscara
        new_width = max(img.width - 2 * padding, 1)
        new_height = max(img.height - 2 * padding, 1)

        # Crear una máscara blanca del nuevo tamaño
        mask = Image.new("RGB", (new_width, new_height), color=(0, 0, 0))

        # Centrar la máscara más pequeña dentro del tamaño original
        final_mask = Image.new("RGB", img.size, color=(255, 255, 255))  # Fondo negro
        final_mask.paste(mask, (padding, padding))

        # Guardar la máscara en formato PNG
        final_mask.save(mask_path, format="PNG")
        print(f"Máscara creada y guardada en: {mask_path}")

    # Validar que la máscara sea compatible
    with Image.open(mask_path) as mask, Image.open(image_path) as img:
        if mask.size != img.size:
            raise Exception("El tamaño de la máscara no coincide con el tamaño de la imagen.")
        if mask.mode not in ["L", "RGB", "RGBA"]:
            raise Exception(f"El formato de la máscara ({mask.mode}) no es compatible.")
        
        print("La máscara es válida y coincide con la imagen.")

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
    """Descarga una imagen desde una URL y la guarda localmente."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen descargada: {save_path}")
    else:
        raise Exception(f"Error al descargar la imagen desde {url}. Código: {response.status_code}")

def delete_file(file_path):
    """Elimina un archivo localmente."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo eliminado: {file_path}")
    except Exception as e:
        print(f"Error al eliminar el archivo {file_path}: {e}")
        

def edit_image(arguments, context):
    """Realiza la edición de una imagen utilizando la API y presenta los parámetros utilizados."""
    
    # Determinar qué imagen usar: proporcionada por el usuario o generada previamente
    image_url = context.get("last_provided_image_url") or context.get("last_generated_image_url")

    if not image_url:
        print("\nNo se encontró ninguna imagen para editar.")
        return {"error": "No se encontró ninguna imagen para editar."}

    arguments["image_url"] = image_url
    print(f"\nSe usará la imagen para la edición: {image_url}")
    
    # URLs y rutas de archivos temporales
    temp_image_path = "temp_image.jpg"
    temp_mask_path = "temp_mask.png"

    try:
        # Descargar la imagen desde la URL
        print("\nDescargando la imagen original...")
        download_image(image_url, temp_image_path)

        # Crear una máscara completa
        print("Creando la máscara para la edición...")
        create_full_mask(temp_image_path, temp_mask_path)

        # Preparar la solicitud a la API
        print("Preparando los datos para la edición...")
        url = "https://api.ideogram.ai/edit"
        headers = {
            "Api-Key": os.getenv("IDEOGRAM_API_KEY")
        }

        files = {
            "image_file": open(temp_image_path, "rb"),
            "mask": open(temp_mask_path, "rb")
        }

        payload = {
            "prompt": arguments["prompt"],
            "model": arguments["model"]
        }

        optional_fields = [
            "magic_prompt_option",
            "seed",
            "style_type"
        ]

        for field in optional_fields:
            if field in arguments and arguments[field] is not None:
                payload[field] = arguments[field]

        response = requests.post(url, data=payload, files=files, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error en la API: {response.text}")

        # Procesar la respuesta
        response_data = response.json()
        edited_url = response_data.get("data", [{}])[0].get("url")
        if edited_url:
            context["last_generated_image_url"] = edited_url
            print(f"\nURL de la imagen editada: {edited_url}\n")
        else:
            print("\nNo se pudo obtener la URL de la imagen editada.")

        return response_data

    finally:
        # Eliminar archivos temporales
        delete_file(temp_image_path)
        delete_file(temp_mask_path)
