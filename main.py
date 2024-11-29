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
    generate_image_function,
    edit_image_function,
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

def iterative_decision_loop(context, iterative=False):
    function_calling_functions = [
        generate_image_function,
        edit_image_function,
        describe_image_function,
        remix_image_function,
        upscale_image_function
    ]
    while True:
        if not iterative:
            user_input = input("\nDescribe lo que necesitas: ")
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("Finalizando la interacción. ¡Hasta luego!")
                break

            # Add user message to messages and history
            messages.append({"role": "user", "content": user_input})
            history.append(f"Usuario: {user_input}")
        else:
            # If iterative, use the last user message
            user_input = messages[-1]["content"]

        # Print current messages
        print("\nMensajes enviados al modelo:")
        for msg in messages:
            print(msg)

        # Detect if the user provided an explicit URL
        url_match = contains_url(user_input)
        if url_match:
            context["last_generated_image_url"] = url_match.group(0)
            print(f"Se detectó que el usuario proporcionó una nueva URL: {context['last_generated_image_url']}")

        # Call the decision function
        print("\nLlamando a openai.ChatCompletion.create()...")
        decision_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            functions=function_calling_functions,
            function_call="auto"
        )
        print("\nRespuesta de OpenAI:")
        print(decision_response)

        decision_message = decision_response["choices"][0]["message"]

        if "function_call" in decision_message:
            function_call = decision_message["function_call"]
            name = function_call["name"]
            arguments_json = function_call["arguments"]
            print(f"\nFunction call detectada: {name}")
            print(f"Arguments JSON: {arguments_json}")
            arguments = json.loads(arguments_json)
            print(f"Arguments dict: {arguments}")

            # Add the last image URL if needed
            last_image_url = context.get("last_generated_image_url")
            if last_image_url and "image_url" in function_calling_functions[
                [func["name"] for func in function_calling_functions].index(name)
            ]["parameters"]["properties"]:
                if "image_url" not in arguments:
                    arguments["image_url"] = last_image_url
                    print(f"Agregando 'image_url' a los argumentos: {last_image_url}")

            # Interpret user's decision
            if name == "adjust_parameters" and not iterative:
                print(f"Se va a realizar {name} con los siguientes parámetros autogenerados:\n{arguments}")
                new_input = input("\n¿Deseas agregar algo más?: ")
                messages.append({"role": "user", "content": new_input})
                history.append(f"Usuario: {new_input}")
                # Recursive call with iterative=True
                iterative_decision_loop(context, iterative=True)
                break

            elif name in ["generate_image", "edit_image", "describe_image", "remix_image", "upscale_image"]:
                print(f"Se va a ejecutar la función {name}")
                # Map function name to action
                action_map = {
                    "generate_image": "generate",
                    "edit_image": "edit",
                    "describe_image": "describe",
                    "remix_image": "remix",
                    "upscale_image": "upscale"
                }
                action = action_map.get(name)
                handle_image_action(action, arguments, context, history)
                # Add assistant's response to messages
                assistant_message = {
                    "role": "assistant",
                    "content": f"Acción '{action}' completada exitosamente. URL de la imagen: {context.get('last_generated_image_url', 'No disponible')}"
                }
                messages.append(assistant_message)
                history.append(f"Asistente: {assistant_message['content']}")
                # Reset iterative
                iterative = False

        else:
            # Handle normal interaction if no specific action
            assistant_response = decision_message["content"]
            print(f"Asistente: {assistant_response}")
            history.append(f"Asistente: {assistant_response}")
            messages.append({"role": "assistant", "content": assistant_response})
            iterative = False

def main():
    """
    Runs the main program loop.
    """
    context = {}
    iterative_decision_loop(context)

if __name__ == "__main__":
    main()
