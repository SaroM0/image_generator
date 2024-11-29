# Function Definitions for Function Calling with OpenAI

confirm_parameters_function = {
    "name": "adjust_or_proceed",
    "description": (
        "Determina si se debe proceder con la acción actual utilizando los parámetros existentes o si "
        "los parámetros requieren ajustes adicionales. Utiliza el contexto proporcionado y el mensaje "
        "del usuario para tomar esta decisión."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "description": (
                    "La decisión a tomar basada en los parámetros actuales: "
                    "'continue_with_image_action' para proceder con la acción actual, o "
                    "'adjust_parameters' si se necesita más información o ajustes de los parámetros."
                ),
                "enum": ["continue_with_image_action", "adjust_parameters"]
            }
        },
        "required": ["decision"]
    }
}

generate_image_function = {
    "name": "generate_image",
    "description": "Genera una nueva imagen basándose en un prompt y opciones específicas.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "El prompt que describe la imagen a generar.",
                "required": True
            },
            "aspect_ratio": {
                "type": "string",
                "description": "Relación de aspecto para la generación de imágenes. No puede usarse junto con 'resolution'.",
                "enum": [
                    "ASPECT_1_1", "ASPECT_16_9", "ASPECT_9_16",
                    "ASPECT_4_3", "ASPECT_3_4", "ASPECT_10_16",
                    "ASPECT_16_10", "ASPECT_3_2", "ASPECT_2_3",
                    "ASPECT_1_3", "ASPECT_3_1"
                ]
            },
            "model": {
                "type": "string",
                "description": "El modelo utilizado para generar la imagen.",
                "enum": ["V_1", "V_1_TURBO", "V_2", "V_2_TURBO"],
                "default": "V_2"
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt para mejorar el prompt.",
                "enum": ["AUTO", "ON", "OFF"],
                "default": "AUTO"
            },
            "seed": {
                "type": "integer",
                "description": "Semilla para la generación reproducible. Debe estar entre 0 y 2147483647.",
                "minimum": 0,
                "maximum": 2147483647
            },
            "style_type": {
                "type": "string",
                "description": "Estilo de la imagen generada. Solo aplicable para modelos V_2 y superiores.",
                "enum": ["AUTO", "GENERAL", "REALISTIC", "DESIGN", "RENDER_3D", "ANIME"]
            },
            "negative_prompt": {
                "type": "string",
                "description": "Descripción de lo que se debe excluir de la imagen. Sobrescribe descripciones en el prompt principal."
            },
            "resolution": {
                "type": "string",
                "description": "Resolución específica de la imagen generada. No puede usarse junto con 'aspect_ratio'.",
                "enum": [
                    "RESOLUTION_512_1536", "RESOLUTION_576_1408", "RESOLUTION_576_1472",
                    "RESOLUTION_576_1536", "RESOLUTION_640_1024", "RESOLUTION_640_1344",
                    "RESOLUTION_640_1408", "RESOLUTION_640_1472", "RESOLUTION_640_1536",
                    "RESOLUTION_704_1152", "RESOLUTION_704_1216", "RESOLUTION_704_1280",
                    "RESOLUTION_704_1344", "RESOLUTION_704_1408", "RESOLUTION_704_1472",
                    "RESOLUTION_720_1280", "RESOLUTION_736_1312", "RESOLUTION_768_1024",
                    "RESOLUTION_768_1088", "RESOLUTION_768_1152", "RESOLUTION_768_1216",
                    "RESOLUTION_768_1232", "RESOLUTION_768_1280", "RESOLUTION_768_1344",
                    "RESOLUTION_832_960", "RESOLUTION_832_1024", "RESOLUTION_832_1088",
                    "RESOLUTION_832_1152", "RESOLUTION_832_1216", "RESOLUTION_832_1248",
                    "RESOLUTION_864_1152", "RESOLUTION_896_960", "RESOLUTION_896_1024",
                    "RESOLUTION_896_1088", "RESOLUTION_896_1120", "RESOLUTION_896_1152",
                    "RESOLUTION_960_832", "RESOLUTION_960_896", "RESOLUTION_960_1024",
                    "RESOLUTION_960_1088", "RESOLUTION_1024_640", "RESOLUTION_1024_768",
                    "RESOLUTION_1024_832", "RESOLUTION_1024_896", "RESOLUTION_1024_960",
                    "RESOLUTION_1024_1024", "RESOLUTION_1088_768", "RESOLUTION_1088_832",
                    "RESOLUTION_1088_896", "RESOLUTION_1088_960", "RESOLUTION_1120_896",
                    "RESOLUTION_1152_704", "RESOLUTION_1152_768", "RESOLUTION_1152_832",
                    "RESOLUTION_1152_864", "RESOLUTION_1152_896", "RESOLUTION_1216_704",
                    "RESOLUTION_1216_768", "RESOLUTION_1216_832", "RESOLUTION_1232_768",
                    "RESOLUTION_1248_832", "RESOLUTION_1280_704", "RESOLUTION_1280_720",
                    "RESOLUTION_1280_768", "RESOLUTION_1280_800", "RESOLUTION_1312_736",
                    "RESOLUTION_1344_640", "RESOLUTION_1344_704", "RESOLUTION_1344_768",
                    "RESOLUTION_1408_576", "RESOLUTION_1408_640", "RESOLUTION_1408_704",
                    "RESOLUTION_1472_576", "RESOLUTION_1472_640", "RESOLUTION_1472_704",
                    "RESOLUTION_1536_512", "RESOLUTION_1536_576", "RESOLUTION_1536_640"
                ]
            },
            "color_palette": {
                "type": "object",
                "description": "Paleta de colores utilizada para la generación. Puede definirse mediante un nombre predefinido o una lista de colores.",
                "oneOf": [
                    {
                        "properties": {
                            "name": {
                                "type": "string",
                                "enum": ["EMBER", "FRESH", "JUNGLE", "MAGIC", "MELON", "MOSAIC", "PASTEL", "ULTRAMARINE"]
                            }
                        },
                        "required": ["name"]
                    },
                    {
                        "properties": {
                            "members": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "color_hex": {
                                            "type": "string",
                                            "description": "Color en formato hexadecimal (e.g., #FFA500).",
                                            "pattern": "^#(?:[0-9a-fA-F]{3}){1,2}$"
                                        },
                                        "color_weight": {
                                            "type": "number",
                                            "description": "Peso del color en la paleta, entre 0.05 y 1.0.",
                                            "minimum": 0.05,
                                            "maximum": 1.0
                                        }
                                    },
                                    "required": ["color_hex"]
                                }
                            }
                        },
                        "required": ["members"]
                    }
                ]
            }
        },
        "required": ["prompt", "model", "style_type", "resolution", "color_palette"]
    }
}

edit_image_function = {
    "name": "edit_image",
    "description": "Edita una imagen existente utilizando un prompt, una máscara y parámetros opcionales.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Descripción de los cambios en la imagen. Este es el prompt utilizado para describir el resultado editado.",
                "required": True
            },
            "image_url": {
                "type": "string",
                "description": "URL de la imagen que se va a editar.",
                "required": True
            },
            "model": {
                "type": "string",
                "description": "El modelo utilizado para la edición. Solo compatible con V_2 y V_2_TURBO.",
                "enum": ["V_2", "V_2_TURBO"],
                "required": True
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt para mejorar el prompt.",
                "enum": ["AUTO", "ON", "OFF"],
                "default": "AUTO"
            },
            "seed": {
                "type": "integer",
                "description": "Semilla para la edición reproducible. Debe estar entre 0 y 2147483647.",
                "minimum": 0,
                "maximum": 2147483647
            },
            "style_type": {
                "type": "string",
                "description": "Estilo de la edición aplicada. Solo aplicable para modelos V_2 y superiores.",
                "enum": ["AUTO", "GENERAL", "REALISTIC", "DESIGN", "RENDER_3D", "ANIME"]
            }
        },
        "required": ["prompt", "image_url", "model"]
    }
}


describe_image_function = {
    "name": "describe_image",
    "description": "Genera una descripción detallada para una imagen proporcionada.",
    "parameters": {
        "type": "object",
        "properties": {
            "image_url": {
                "type": "string",
                "description": "URL de la imagen a describir"
            }
        },
        "required": ["image_url"]
    },
    "response": {
        "type": "object",
        "properties": {
            "descriptions": {
                "type": "array",
                "description": "Una colección de descripciones generadas para el contenido proporcionado.",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "La descripción generada para la imagen proporcionada."
                        }
                    }
                }
            }
        }
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
                "description": "Descripción del remix deseado. Este es un campo obligatorio."
            },
            "image_url": {
                "type": "string",
                "description": "URL de la imagen que se va a remixar. Este es un campo obligatorio."
            },
            "aspect_ratio": {
                "type": "string",
                "description": "Relación de aspecto para la imagen remixada.",
                "enum": [
                    "ASPECT_1_1",
                    "ASPECT_16_9",
                    "ASPECT_9_16",
                    "ASPECT_4_3",
                    "ASPECT_3_4",
                    "ASPECT_10_16",
                    "ASPECT_16_10",
                    "ASPECT_3_2",
                    "ASPECT_2_3",
                    "ASPECT_1_3",
                    "ASPECT_3_1"
                ]
            },
            "color_palette": {
                "type": "object",
                "description": "Paleta de colores utilizada para el remix. Puede ser un preset o colores personalizados.",
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
                                    "description": "Color en formato hexadecimal.",
                                    "pattern": "^#(?:[0-9a-fA-F]{3}){1,2}$"
                                },
                                "color_weight": {
                                    "type": "number",
                                    "description": "Peso del color en la paleta.",
                                    "minimum": 0.05,
                                    "maximum": 1.0
                                }
                            },
                            "required": ["color_hex"]
                        }
                    }
                }
            },
            "image_weight": {
                "type": "integer",
                "description": "Peso de la imagen base en la generación.",
                "minimum": 1,
                "maximum": 100,
                "default": 50
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt para mejorar el prompt.",
                "enum": ["AUTO", "ON", "OFF"],
                "default": "AUTO"
            },
            "model": {
                "type": "string",
                "description": "Modelo utilizado para el remix.",
                "enum": ["V_1", "V_1_TURBO", "V_2", "V_2_TURBO"],
                "default": "V_2"
            },
            "negative_prompt": {
                "type": "string",
                "description": "Descripción de lo que se debe excluir de la imagen."
            },
            "resolution": {
                "type": "string",
                "description": "Resolución específica de la imagen generada.",
                "enum": [
                    "RESOLUTION_512_1536", "RESOLUTION_576_1408", "RESOLUTION_576_1472", "RESOLUTION_576_1536",
                    "RESOLUTION_640_1024", "RESOLUTION_640_1344", "RESOLUTION_640_1408", "RESOLUTION_640_1472",
                    "RESOLUTION_640_1536", "RESOLUTION_704_1152", "RESOLUTION_704_1216", "RESOLUTION_704_1280",
                    "RESOLUTION_704_1344", "RESOLUTION_704_1408", "RESOLUTION_704_1472", "RESOLUTION_720_1280",
                    "RESOLUTION_736_1312", "RESOLUTION_768_1024", "RESOLUTION_768_1088", "RESOLUTION_768_1152",
                    "RESOLUTION_768_1216", "RESOLUTION_768_1232", "RESOLUTION_768_1280", "RESOLUTION_768_1344",
                    "RESOLUTION_832_960", "RESOLUTION_832_1024", "RESOLUTION_832_1088", "RESOLUTION_832_1152",
                    "RESOLUTION_832_1216", "RESOLUTION_832_1248", "RESOLUTION_864_1152", "RESOLUTION_896_960",
                    "RESOLUTION_896_1024", "RESOLUTION_896_1088", "RESOLUTION_896_1120", "RESOLUTION_896_1152",
                    "RESOLUTION_960_832", "RESOLUTION_960_896", "RESOLUTION_960_1024", "RESOLUTION_960_1088",
                    "RESOLUTION_1024_640", "RESOLUTION_1024_768", "RESOLUTION_1024_832", "RESOLUTION_1024_896",
                    "RESOLUTION_1024_960", "RESOLUTION_1024_1024", "RESOLUTION_1088_768", "RESOLUTION_1088_832",
                    "RESOLUTION_1088_896", "RESOLUTION_1088_960", "RESOLUTION_1120_896", "RESOLUTION_1152_704",
                    "RESOLUTION_1152_768", "RESOLUTION_1152_832", "RESOLUTION_1152_864", "RESOLUTION_1152_896",
                    "RESOLUTION_1216_704", "RESOLUTION_1216_768", "RESOLUTION_1216_832", "RESOLUTION_1232_768",
                    "RESOLUTION_1248_832", "RESOLUTION_1280_704", "RESOLUTION_1280_720", "RESOLUTION_1280_768",
                    "RESOLUTION_1280_800", "RESOLUTION_1312_736", "RESOLUTION_1344_640", "RESOLUTION_1344_704",
                    "RESOLUTION_1344_768", "RESOLUTION_1408_576", "RESOLUTION_1408_640", "RESOLUTION_1408_704",
                    "RESOLUTION_1472_576", "RESOLUTION_1472_640", "RESOLUTION_1472_704", "RESOLUTION_1536_512",
                    "RESOLUTION_1536_576", "RESOLUTION_1536_640"
                ]
            },
            "seed": {
                "type": "integer",
                "description": "Semilla para la generación reproducible.",
                "minimum": 0,
                "maximum": 2147483647
            },
            "style_type": {
                "type": "string",
                "description": "Estilo del remix aplicado.",
                "enum": ["AUTO", "GENERAL", "REALISTIC", "DESIGN", "RENDER_3D", "ANIME"],
                "default": "AUTO"
            }
        },
        "required": ["prompt", "image_url"]
    }
}

upscale_image_function = {
    "name": "upscale_image",
    "description": "Aumenta la resolución de una imagen proporcionada con parámetros opcionales.",
    "parameters": {
        "type": "object",
        "properties": {
            "image_url": {
                "type": "string",
                "description": "URL de la imagen que se va a escalar. Este es un campo obligatorio."
            },
            "prompt": {
                "type": "string",
                "description": "Prompt opcional para guiar el proceso de escalado."
            },
            "resemblance": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "default": 50,
                "description": "Nivel de semejanza con la imagen original (1-100)."
            },
            "detail": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "default": 50,
                "description": "Nivel de detalle en la imagen escalada (1-100)."
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Activa o desactiva MagicPrompt.",
                "enum": ["AUTO", "ON", "OFF"],
                "default": "AUTO"
            },
            "seed": {
                "type": "integer",
                "minimum": 0,
                "maximum": 2147483647,
                "description": "Semilla para la generación reproducible."
            }
        },
        "required": ["image_url"]
    }
}
