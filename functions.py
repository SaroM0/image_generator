import re
from api_functions.generate import generate_image
from api_functions.describe import describe_image
from api_functions.upscale import upscale_image
from api_functions.remix import remix_image
from api_functions.edit import edit_image

# Detectar si el texto contiene una URL
def contains_url(text):
    """Detecta si el texto contiene una URL."""
    url_pattern = re.compile(r'(https?://\S+)')
    return url_pattern.search(text)

# Manejar las acciones relacionadas con imágenes
def handle_image_action(action, arguments, context, history):
    """
    Ejecuta la acción correspondiente según la decisión detectada.
    """
    print(f"\nArgumentos antes de limpiar: {arguments}")
    arguments = clean_arguments(arguments, action, context)
    print(f"Argumentos después de limpiar: {arguments}")

    if action == "generate":
        print("\nGenerando imagen con los siguientes parámetros:")
        print(arguments)
        result = generate_image(arguments, context)
    elif action == "edit":
        print("\nEditando imagen con los siguientes parámetros:")
        print(arguments)
        result = edit_image(arguments, context)
    elif action == "upscale":
        print("\nEscalando imagen con los siguientes parámetros:")
        print(arguments)
        result = upscale_image(arguments, context)
    elif action == "describe":
        print("\nDescribiendo imagen con los siguientes parámetros:")
        print(arguments)
        result = describe_image(arguments, context)
    elif action == "remix":
        print("\nRemixando imagen con los siguientes parámetros:")
        print(arguments)
        result = remix_image(arguments, context)
    else:
        print(f"Acción desconocida: {action}")
        return

    # Actualizar contexto con el resultado
    url = result.get("url", "No disponible")
    print(f"\n¡Acción '{action}' completada exitosamente!")
    print(f"URL de la imagen: {url}")
    history.append(f"Asistente: Acción '{action}' completada con éxito. URL: {url}")
    context["last_generated_image_url"] = url  # Actualizar la última URL en el contexto

# Limpieza y validación de argumentos
def clean_arguments(arguments, action, context):
    """
    Limpia y valida los argumentos antes de llamar a la API.
    """
    # Eliminar parámetros con valor None
    arguments = {k: v for k, v in arguments.items() if v is not None}

    # Manejar 'color_palette'
    if 'color_palette' in arguments:
        color_palette = arguments['color_palette']
        if 'name' in color_palette and 'members' in color_palette:
            print("Eliminando 'members' de 'color_palette' porque ambos 'name' y 'members' están presentes.")
            del color_palette['members']
        arguments['color_palette'] = color_palette

    # Añadir 'image_url' si falta y está disponible en el contexto
    if action in ['edit', 'remix', 'upscale', 'describe'] and 'image_url' not in arguments:
        last_image_url = context.get("last_generated_image_url")
        if last_image_url:
            arguments['image_url'] = last_image_url
            print(f"Agregando 'image_url' a los argumentos: {last_image_url}")
        else:
            print("No se proporcionó 'image_url' y no hay una URL de imagen previa.")
            return arguments

    return arguments
