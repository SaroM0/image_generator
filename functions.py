from PIL import Image
import numpy as np
import requests
import os


context = {
    "last_generated_image_url": None,  # Imagen generada por el modelo
    "last_provided_image_url": None,   # Imagen proporcionada manualmente
}

def detect_provided_image(user_input):
    """
    Detecta si el usuario proporcionó una URL de imagen en su entrada.
    Si encuentra una URL válida, la guarda en el contexto.
    """
    if "http" in user_input:
        words = user_input.split()
        for word in words:
            if word.startswith("http"):
                context["last_provided_image_url"] = word
                print(f"Se actualizó la imagen proporcionada por el usuario: {context['last_provided_image_url']}")
                return True
    return False


def decide_action(arguments):
    """Determina la acción a tomar según el argumento proporcionado."""
    action = arguments["action"]
    if action == "generate":
        print("Se determinó que se debe generar una imagen.")
        return "generate"
    elif action == "edit":
        print("Se determinó que se debe editar una imagen.")
        return "edit"
    else:
        print("No se realizará ninguna acción auxiliar.")
        return "none"



def confirm_parameters(arguments):
    """Muestra los parámetros al usuario y confirma si desea proceder."""
    print("\nEstos son los parámetros con los que se generará la imagen:")
    for key, value in arguments.items():
        # Reemplazar 'image_url' con el valor almacenado en el contexto
        if key == "image_url":
            value = context.get("last_provided_image_url") or context.get("last_generated_image_url") or "No especificado"
        print(f"  {key}: {value if value else 'No especificado'}")
    
    confirm = input("\n¿Deseas proceder a generar la imagen con estos parámetros? (s/n): ")
    if confirm.lower() != 's':
        edit = input("¿Quieres editar los parámetros? (s/n): ")
        if edit.lower() == 's':
            for key in arguments.keys():
                new_value = input(f"Introduce un nuevo valor para '{key}' (deja vacío para mantener el actual): ")
                if new_value:
                    arguments[key] = new_value
            return True
        return False
    return True




def generate_image(arguments):
    """Genera una imagen utilizando la API de Ideogram."""
    url = "https://api.ideogram.ai/generate"
    headers = {
        "Api-Key": os.getenv("IDEOGRAM_API_KEY"),
        "Content-Type": "application/json"
    }

    # Construir la carga útil dinámicamente para incluir solo campos definidos
    payload = {
        "image_request": {
            "prompt": arguments["prompt"],  # Campo requerido
        }
    }

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

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en la API: {response.text}")

    # Procesar la respuesta
    response_data = response.json()

    if "data" in response_data and response_data["data"]:
        generated_url = response_data["data"][0].get("url")
        if generated_url:
            context["last_generated_image_url"] = generated_url
            print(f"\nURL de la imagen generada: {generated_url}\n")
        else:
            print("\nNo se pudo obtener la URL de la imagen generada.")
    else:
        print("\nNo se pudo generar la imagen.")

    return response_data




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
    
# La mask debe ser un poco más pequeña que la imagen
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

def delete_file(file_path):
    """Elimina un archivo localmente."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo eliminado: {file_path}")
    except Exception as e:
        print(f"Error al eliminar el archivo {file_path}: {e}")
        

def edit_image(arguments):
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