import openai
from openai_client import initialize_openai
from functions import  detect_provided_image, decide_action, confirm_parameters, generate_image, edit_image
from function_calling import decision_function, generate_image_function, edit_image_function
from dotenv import load_dotenv
import json

load_dotenv()
initialize_openai()

def display_history(history):
    """Muestra un pequeño historial de la conversación."""
    print("\n--- Historial de conversación ---")
    for i, entry in enumerate(history, 1):
        print(f"{i}. {entry}")
    print("-------------------------------")
    

def main():
    print("Prueba de concepto - generación y edición de imágenes con contexto.")
    
    # Mensajes iniciales del sistema
    messages = [
        {
            "role": "system",
            "content": (
                "Eres un asistente que ayuda a los usuarios a generar o editar imágenes mediante una API. "
                "Primero, decide si la consulta del usuario requiere una generación, una edición, o ninguna acción."
            )
        }
    ]

    # Historial de conversación
    history = []

    while True:
        user_input = input("\nDescribe lo que necesitas (generar o editar una imagen, o simplemente haz preguntas): ")
        
        if detect_provided_image(user_input):
            print("La entrada contiene una URL de imagen. Continuando con la edición...")
            continue  # Saltar al siguiente ciclo para manejar esta URL en otra entrada

        
        messages.append({"role": "user", "content": user_input})
        history.append(f"Usuario: {user_input}")

        # Primera decisión: determinar si se debe generar, editar o ninguna acción
        decision_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            functions=[decision_function],
            function_call="auto"
        )

        decision_message = decision_response["choices"][0]["message"]

        if "function_call" in decision_message:
            function_call = decision_message["function_call"]
            decision_arguments = json.loads(function_call["arguments"])
            action = decide_action(decision_arguments)

            if action == "generate":
                # Llamar a la función para generación de imágenes
                response = openai.ChatCompletion.create(
                    model="gpt-4-0613",
                    messages=messages,
                    functions=[generate_image_function],
                    function_call="auto"
                )
                handle_generate_image(response, messages, history)

            elif action == "edit":
                # Llamar a la función para edición de imágenes
                response = openai.ChatCompletion.create(
                    model="gpt-4-0613",
                    messages=messages,
                    functions=[edit_image_function],
                    function_call="auto"
                )
                handle_edit_image(response, messages, history)

        else:
            # Continuar con la conversación normal
            assistant_response = decision_message["content"]
            print(f"Asistente: {assistant_response}")
            history.append(f"Asistente: {assistant_response}")
            user_input = input("Respuesta: ")
            messages.append({"role": "user", "content": user_input})
            history.append(f"Usuario: {user_input}")

        # Mostrar historial actualizado
        display_history(history)

        print("\nPuedes seguir describiendo imágenes, editarlas o simplemente hacer preguntas.")

# Función para manejar la generación de imágenes
def handle_generate_image(response, messages, history):
    message = response["choices"][0]["message"]
    if "function_call" in message:
        function_call = message["function_call"]
        arguments = json.loads(function_call["arguments"])

        if confirm_parameters(arguments):
            try:
                image_response = generate_image(arguments)
                print("\n¡Imagen generada exitosamente!")
                print(json.dumps(image_response, indent=2))
                
                response_message = "La imagen ha sido generada con éxito."
                messages.append({"role": "assistant", "content": response_message})
                history.append(f"Asistente: {response_message} - Parámetros: {arguments}")
            except Exception as e:
                error_message = f"Ocurrió un error al generar la imagen: {e}"
                print(error_message)
                messages.append({"role": "assistant", "content": error_message})
                history.append(f"Asistente: {error_message}")

# Función para manejar la edición de imágenes
def handle_edit_image(response, messages, history):
    message = response["choices"][0]["message"]
    if "function_call" in message:
        function_call = message["function_call"]
        arguments = json.loads(function_call["arguments"])

        if confirm_parameters(arguments):
            try:
                edit_response = edit_image(arguments)
                print("\n¡Imagen editada exitosamente!")
                print(json.dumps(edit_response, indent=2))
                
                response_message = "La imagen ha sido editada con éxito."
                messages.append({"role": "assistant", "content": response_message})
                history.append(f"Asistente: {response_message} - Parámetros: {arguments}")
            except Exception as e:
                error_message = f"Ocurrió un error al editar la imagen: {e}"
                print(error_message)
                messages.append({"role": "assistant", "content": error_message})
                history.append(f"Asistente: {error_message}")

if __name__ == "__main__":
    main()
