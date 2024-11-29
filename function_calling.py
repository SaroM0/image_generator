# Function Definitions for Function Calling with OpenAI

generate_image_function = {
    "name": "generate_image",
    "description": "Genera una nueva imagen basándose en un prompt y opciones específicas.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "El prompt que describe la imagen a generar."
            },
            "aspect_ratio": {
                "type": "string",
                "description": "Relación de aspecto para la generación de imágenes.",
                "enum": [
                    "ASPECT_1_1",
                    "ASPECT_16_9",
                    "ASPECT_9_16",
                    "ASPECT_4_3",
                    "ASPECT_3_4"
                ]
            },
            "model": {
                "type": "string",
                "description": "El modelo utilizado para generar la imagen.",
                "enum": ["V_1", "V_1_TURBO", "V_2", "V_2_TURBO"]
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt para mejorar el prompt.",
                "enum": ["AUTO", "ON", "OFF"]
            },
            "seed": {
                "type": "integer",
                "description": "Semilla para la generación reproducible."
            },
            "style_type": {
                "type": "string",
                "description": "Estilo de la imagen generada.",
                "enum": ["AUTO", "GENERAL", "REALISTIC", "ANIME", "DESIGN", "RENDER_3D"]
            },
            "negative_prompt": {
                "type": "string",
                "description": "Descripción de lo que se debe excluir de la imagen."
            },
            "resolution": {
                "type": "string",
                "description": "Resolución específica de la imagen generada."
            },
            "color_palette": {
                "type": "object",
                "description": "Paleta de colores utilizada para la generación.",
                "properties": {
                    "name": {
                        "type": "string",
                        "enum": ["EMBER", "FRESH", "JUNGLE", "MAGIC", "MELON", "MOSAIC", "PASTEL", "ULTRAMARINE"]
                    },
                    "members": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "color_hex": {
                                    "type": "string",
                                    "description": "Color en formato hexadecimal."
                                },
                                "color_weight": {
                                    "type": "number",
                                    "minimum": 0.05,
                                    "maximum": 1.0,
                                    "description": "Peso del color en la paleta."
                                }
                            },
                            "required": ["color_hex"]
                        }
                    }
                }
            }
        },
        "required": ["prompt"]
    }
}

edit_image_function = {
    "name": "edit_image",
    "description": "Edita una imagen existente utilizando un prompt y una máscara.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Descripción de los cambios en la imagen."
            },
            "image_url": {
                "type": "string",
                "description": "URL de la imagen que se va a editar."
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt para mejorar el prompt.",
                "enum": ["AUTO", "ON", "OFF"]
            },
            "model": {
                "type": "string",
                "description": "Modelo utilizado para la edición.",
                "enum": ["V_2", "V_2_TURBO"]
            },
            "style_type": {
                "type": "string",
                "description": "Estilo de la edición aplicada.",
                "enum": ["REALISTIC", "ANIME", "DESIGN", "RENDER_3D"]
            },
        },
        "required": ["prompt", "image_url"]
    }
}

describe_image_function = {
    "name": "describe_image",
    "description": "Genera una descripción para una imagen proporcionada.",
    "parameters": {
        "type": "object",
        "properties": {
            "image_url": {
                "type": "string",
                "description": "URL de la imagen a describir."
            }
        },
        "required": ["image_url"]
    }
}

remix_image_function = {
    "name": "remix_image",
    "description": "Realiza un remix de una imagen basada en un prompt y parámetros opcionales.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Descripción del remix deseado."
            },
            "image_url": {
                "type": "string",
                "description": "URL de la imagen que se va a remixar."
            },
            "aspect_ratio": {
                "type": "string",
                "description": "Relación de aspecto para la imagen remixada.",
                "enum": [
                    "ASPECT_1_1",
                    "ASPECT_16_9",
                    "ASPECT_9_16",
                    "ASPECT_4_3",
                    "ASPECT_3_4"
                ]
            },
            "image_weight": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "description": "Peso de la imagen base en la generación."
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt.",
                "enum": ["AUTO", "ON", "OFF"]
            },
            "model": {
                "type": "string",
                "description": "Modelo utilizado para la generación del remix.",
                "enum": ["V_2", "V_2_TURBO"]
            }
        },
        "required": ["prompt", "image_url"]
    }
}

upscale_image_function = {
    "name": "upscale_image",
    "description": "Aumenta la resolución de una imagen proporcionada.",
    "parameters": {
        "type": "object",
        "properties": {
            "image_url": {
                "type": "string",
                "description": "URL de la imagen que se va a escalar."
            },
            "resemblance": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "description": "Nivel de semejanza con la imagen original (1-100)."
            },
            "detail": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "description": "Nivel de detalle en la imagen escalada (1-100)."
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt.",
                "enum": ["AUTO", "ON", "OFF"]
            },
            "seed": {
                "type": "integer",
                "description": "Semilla para la generación reproducible."
            }
        },
        "required": ["image_url"]
    }
}
