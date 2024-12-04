# General Imports
from dotenv import load_dotenv
import openai
import json

# OpenAI Client Import
from openai_client import initialize_openai

# Common Functions Imports
from functions import contains_url, handle_image_action

# Function Calling Imports
from function_calling import (
    confirm_parameters_function,
    generate_image_function,
    describe_image_function,
    remix_image_function,
    upscale_image_function
)

# Load environment variables and initialize OpenAI
load_dotenv()
initialize_openai()

# Initialize global context and messages
context = {}
messages = [
    {
        "role": "system",
        "content": (
            "Eres un asistente que puede analizar prompts y realizar acciones como generar, editar, escalar o describir imágenes."
        )
    }
]
history = []

def display_history(history):
    """Displays a brief conversation history."""
    print("\n--- Historial de conversación ---")
    for i, entry in enumerate(history, 1):
        print(f"{i}. {entry}")
    print("-------------------------------")

def iterative_decision_loop():
    # Definir las funciones que estarán disponibles para el modelo
    function_calling_functions = [
        confirm_parameters_function,
        generate_image_function,
        describe_image_function,
        remix_image_function,
        upscale_image_function
    ]

    while True:
        # Solicitar input del usuario
        user_input = input("\nDescribe lo que necesitas: ")
        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("Finalizando la interacción. ¡Hasta luego!")
            break

        # Agregar el mensaje del usuario al historial
        messages.append({"role": "user", "content": user_input})
        history.append(f"Usuario: {user_input}")

        # Llamar al function calling para tomar una decisión
        print("\nLlamando a openai.ChatCompletion.create()...")
        decision_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            functions=function_calling_functions,
            function_call="auto"
        )
        print("\nRespuesta de OpenAI:")
        print(json.dumps(decision_response, indent=4))

        decision_message = decision_response["choices"][0]["message"]

        if "function_call" in decision_message:
            # Detectar la función sugerida
            function_call = decision_message["function_call"]
            name = function_call["name"]
            arguments_json = function_call["arguments"]
            arguments = json.loads(arguments_json)

            # Si se sugiere ajustar o confirmar parámetros
            if name == "adjust_or_proceed":
                function = arguments.get("function")
                print(f"\nSe va a {function} con los siguientes parametros: {arguments}")
                messages.append({"role": "user", "content": arguments})
                history.append(f"Confirmación: {arguments}")
                new_input = input("\nDeseas agregar algo mas?: ")
                messages.append({"role": "user", "content": new_input})
                history.append(f"Usuario: {new_input}")
                iterative_decision_loop()
                break


            # Si el modelo sugiere directamente una función principal
            elif name in ["generate_image", "describe_image", "remix_image", "upscale_image"]:
                print(f"\nEjecutando función: {name}")
                handle_image_action(name, arguments, context, history)

                # Agregar la respuesta del asistente al historial
                assistant_message = {
                    "role": "assistant",
                    "content": f"Acción '{name}' completada exitosamente. URL de la imagen: {context.get('last_generated_image_url', 'No disponible')}"
                }
                messages.append(assistant_message)
                history.append(f"Asistente: {assistant_message['content']}")

        else:
            # Respuesta sin función, respuesta normal del asistente
            assistant_response = decision_message["content"]
            print(f"Asistente: {assistant_response}")
            history.append(f"Asistente: {assistant_response}")
            messages.append({"role": "assistant", "content": assistant_response})


def main():
    """
    Runs the main program loop.
    """
    iterative_decision_loop()

if __name__ == "__main__":
    main()
